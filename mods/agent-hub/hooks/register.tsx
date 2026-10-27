import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { AgentRow, MessageRow, PeerRow } from '../types'

const PANE = 'agent-hub'
const TITLE = 'Agents'

const agents = atom({ plugin: 'agent-hub', key: 'agents' } as const, [] as AgentRow[])
const peers = atom({ plugin: 'agent-hub', key: 'peers' } as const, [] as PeerRow[])
const messages = atom({ plugin: 'agent-hub', key: 'messages' } as const, [] as MessageRow[])
const isRouting = atom({ plugin: 'agent-hub', key: 'isRouting' } as const, true)
const routedCount = atom({ plugin: 'agent-hub', key: 'routedCount' } as const, 0)
const peersCheckedAt = atom({ plugin: 'agent-hub', key: 'peersCheckedAt' } as const, 0)

// Agent types that only read or look things up: always fine on the cheap model.
const CHEAP_TYPES = new Set(['Explore', 'claude-code-guide', 'statusline-setup', 'agent-hub:quick'])
// Words that mark a short task as simple lookup or formatting work.
const SIMPLE_WORDS =
  /\b(find|search|look ?up|list|locate|grep|read|summari[sz]e|count|check|rename|format|convert|translate|extract|lint|typo|spell)\b/i
// Words that mark a task as needing the strong model, whatever its length.
const HARD_WORDS = /\b(design|architect|refactor|debug|implement|build|plan|review|security|migrate)\b/i

function isSimpleJob(subagentType: string, description: string, prompt: string): boolean {
  if (CHEAP_TYPES.has(subagentType)) return true
  const text = `${description} ${prompt}`
  if (HARD_WORDS.test(text)) return false
  return prompt.length < 600 && SIMPLE_WORDS.test(text)
}

function clip(text: string, size: number): string {
  const line = text.replace(/\s+/g, ' ').trim()
  return line.length > size ? `${line.slice(0, size - 1)}…` : line
}

function ago(now: number, at: number): string {
  const s = Math.max(0, Math.round((now - at) / 1000))
  return s < 60 ? `${s}s ago` : `${Math.round(s / 60)}m ago`
}

// Per agent id: the model it was started on and whether it was routed cheap.
const spawned = new Map<string, { model: string; isCheap: boolean }>()
// Per agent id: what its loop last did.
const activity = new Map<string, string>()

async function refreshAgents($: EngineInterface) {
  const list = await $.agent.list()
  const rows: AgentRow[] = list.map(a => ({
    id: a.id,
    name: a.name ?? a.teammateId ?? a.id.slice(0, 8),
    type: a.type,
    status: a.status,
    description: a.description,
    model: spawned.get(a.id)?.model ?? 'inherit',
    isCheap: spawned.get(a.id)?.isCheap ?? false,
    activity: activity.get(a.id) ?? '',
  }))
  await update($, agents, () => rows)
}

async function refreshPeers($: EngineInterface) {
  try {
    const ran = await $.tool.call({ tool: 'ListAgents' })
    const rows: PeerRow[] = []
    type Listing = {
      sections?: { kind: string; rows: { name?: string; ref?: string; id?: string; type?: string; status?: string }[] }[]
    }
    if ('result' in ran && ran.result) {
      for (const section of (ran.result as Listing).sections ?? []) {
        for (const row of section.rows) {
          rows.push({
            name: row.name ?? row.ref ?? row.id ?? '?',
            kind: row.type ?? section.kind,
            status: row.status ?? '',
          })
        }
      }
    }
    await update($, peers, () => rows)
    const checked = await $.clock.now()
    await update($, peersCheckedAt, () => checked)
  } catch {
    // ListAgents is not available everywhere; leave the last listing.
  }
}

async function log($: EngineInterface, row: Omit<MessageRow, 'at'>) {
  const at = await $.clock.now()
  await update($, messages, list => [...list, { ...row, at }].slice(-30))
}

export const register: Register = (on, options) => {
  const cheapModel = String((options as { cheapModel?: string }).cheapModel ?? 'haiku')
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'agent-hub', description: 'Open the agents dashboard pane' })
    await $.command.register({
      name: 'msg',
      description: 'Send a message to another session or agent: /msg <name> <text>',
    })
    await $.command.register({
      name: 'cheap',
      description: 'Cheap-model routing for simple agent jobs: /cheap on | off',
    })
    await $.agent.register({
      name: 'quick',
      description:
        'Fast, low-cost helper for simple jobs: file lookups, searches, short summaries, renames, formatting. Not for design, debugging or multi-step builds.',
      prompt:
        'You are a quick helper. Do the one small job you are given, directly and briefly, and report the result in a few lines.',
      model: cheapModel,
    })
    $.clock.every(5000, () => refreshAgents($))
    $.clock.every(60000, () => refreshPeers($))
    void refreshPeers($)
    void $.ui.open({ id: PANE, title: TITLE })

    return next(e)
  })

  // Tell the main model the quick helper exists, so it delegates simple jobs.
  on('prompt.compose', async ($, e, next) => {
    const composed = await next(e)
    if (!(await read($, isRouting))) return composed

    return {
      ...composed,
      sections: [
        ...composed.sections,
        {
          id: 'agent-hub-routing',
          scope: 'session' as const,
          text: `When a task is a simple job (a lookup, search, short summary, rename or formatting), delegate it to the agent-hub:quick agent, which runs on the cheaper ${cheapModel} model. Keep design, debugging and multi-step work on the main model.`,
        },
      ],
    }
  })

  // Route simple sub-agent jobs to the cheap model, unless a model was named.
  on('agent.spawn', async ($, e, next) => {
    const isCheap =
      e.model === undefined &&
      (await read($, isRouting)) &&
      isSimpleJob(e.subagentType, e.description, e.prompt)
    const ran = await next(isCheap ? { ...e, model: cheapModel } : e)
    if ('agentId' in ran && ran.agentId) {
      spawned.set(ran.agentId, { model: ran.model, isCheap })
      if (isCheap) await update($, routedCount, n => n + 1)
      await refreshAgents($)
    }

    return ran
  })

  // Record what each agent is doing right now.
  on('tool.call', async ($, e, next) => {
    if (e.agentId) {
      const input = e as unknown as Record<string, unknown>
      const detail = input.command ?? input.file_path ?? input.pattern ?? input.query ?? input.url ?? ''
      activity.set(e.agentId, clip(`${e.tool} ${String(detail)}`, 60))
    }

    return next(e)
  })

  on('session.send', async ($, e, next) => {
    const ran = await next(e)
    if (!e.agentId) await log($, { direction: 'out', who: e.to, text: clip(e.text, 120) })

    return ran
  })

  on('session.receive', async ($, e, next) => {
    const kind = e.origin.kind
    if (!e.agentId && (kind === 'peer' || kind === 'peer-send-message' || kind === 'coordinator')) {
      const who = 'teammate' in e.origin ? String(e.origin.teammate) : 'peer'
      await log($, { direction: 'in', who, text: clip(e.text, 120) })
    }

    return next(e)
  })

  on('command.run', { command: 'agent-hub' }, async $ => {
    await $.ui.open({ id: PANE, title: TITLE })
    await refreshAgents($)
    await refreshPeers($)

    return { text: 'Agents dashboard opened.' }
  })

  on('command.run', { command: 'msg' }, async ($, e) => {
    const match = e.args.trim().match(/^(\S+)\s+([\s\S]+)$/)
    if (!match) return { text: 'Usage: /msg <session or agent name> <text>' }
    const to = match[1] ?? ''
    const text = match[2] ?? ''
    const sent = await $.session.send({ to, text })
    if ('deny' in sent && sent.deny) return { text: `Not sent: ${sent.deny}` }

    return { text: `Sent to ${to}.` }
  })

  on('command.run', { command: 'cheap' }, async ($, e) => {
    const arg = e.args.trim().toLowerCase()
    if (arg === 'on' || arg === 'off') await update($, isRouting, () => arg === 'on')
    const isOn = await read($, isRouting)

    return { text: `Cheap-model routing is ${isOn ? `on (${cheapModel})` : 'off'}.` }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const now = await $.clock.now()
    const agentRows = await read($, agents)
    const peerRows = await read($, peers)
    const messageRows = await read($, messages)
    const isOn = await read($, isRouting)
    const routed = await read($, routedCount)
    const checkedAt = await read($, peersCheckedAt)

    return (
      <Box flexDirection="column" gap={1}>
        <Box flexDirection="column">
          <Text bold>Cost routing</Text>
          <Text dimColor>
            Simple jobs → {cheapModel} · {isOn ? 'on' : 'off'} · {routed} routed
          </Text>
          <Button
            key="toggle-routing"
            label={isOn ? 'Turn routing off' : 'Turn routing on'}
            onPress={() => update($, isRouting, v => !v)}
          />
        </Box>

        <Box flexDirection="column">
          <Text bold>This session's agents ({agentRows.length})</Text>
          {agentRows.length === 0 && <Text dimColor>No agents started yet.</Text>}
          {agentRows.map(a => (
            <Box key={a.id} flexDirection="column">
              <Text>
                {a.status === 'running' ? '● ' : '○ '}
                {a.name} · {a.type} · {a.model}
                {a.isCheap ? ' (cheap)' : ''} · {a.status}
              </Text>
              <Text dimColor>  {clip(a.description, 70)}</Text>
              {a.activity !== '' && a.status === 'running' && <Text dimColor>  now: {a.activity}</Text>}
            </Box>
          ))}
        </Box>

        <Box flexDirection="column">
          <Text bold>Other sessions ({peerRows.length})</Text>
          {peerRows.length === 0 && <Text dimColor>None reachable.</Text>}
          {peerRows.map(p => (
            <Text key={`${p.kind}:${p.name}`}>
              {p.name} · {p.kind}
              {p.status ? ` · ${p.status}` : ''}
            </Text>
          ))}
          <Text dimColor>{checkedAt ? `checked ${ago(now, checkedAt)}` : 'not checked yet'}</Text>
          <Button key="refresh-peers" label="Refresh" onPress={() => refreshPeers($)} />
        </Box>

        <Box flexDirection="column">
          <Text bold>Messages</Text>
          {messageRows.length === 0 && <Text dimColor>No messages yet. Send one with /msg &lt;name&gt; &lt;text&gt;.</Text>}
          {messageRows.slice(-10).map(m => (
            <Text key={`${m.at}:${m.who}`}>
              {m.direction === 'out' ? '→' : '←'} {m.who}: {m.text}{' '}
              <Text dimColor>({ago(now, m.at)})</Text>
            </Text>
          ))}
        </Box>
      </Box>
    )
  })
}
