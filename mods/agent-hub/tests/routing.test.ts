import { expect, test } from 'claude-code/testing'

const SPAWN = {
  tool_use_id: 't1',
  parentModel: 'opus',
  provider: { plugin: 'engine', tier: 'core' },
} as const

test('simple jobs go to the cheap model, hard ones stay', async ($, on) => {
  const seen: (string | undefined)[] = []
  on('agent.spawn', (_, e) => {
    seen.push(e.model)
    return { model: e.model ?? 'opus', agentId: `a${seen.length}` }
  })
  on('agent.list', () => ({ value: [] }))

  await $.agent.spawn({ ...SPAWN, prompt: 'Find where the logo file is used', description: 'find logo', subagentType: 'general-purpose' } as never)
  await $.agent.spawn({ ...SPAWN, prompt: 'Refactor the checkout flow and debug the totals', description: 'refactor checkout', subagentType: 'general-purpose' } as never)
  await $.agent.spawn({ ...SPAWN, prompt: 'Look around the repo', description: 'explore', subagentType: 'Explore' } as never)
  await $.agent.spawn({ ...SPAWN, prompt: 'List the files', description: 'list', subagentType: 'general-purpose', model: 'opus' } as never)

  expect(seen).toEqual(['haiku', undefined, 'haiku', 'opus'])
})
