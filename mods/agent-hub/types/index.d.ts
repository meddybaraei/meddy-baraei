export type AgentRow = {
  id: string
  name: string
  type: string
  status: string
  description: string
  model: string
  isCheap: boolean
  activity: string
}

export type PeerRow = { name: string; kind: string; status: string }

export type MessageRow = { at: number; direction: 'in' | 'out'; who: string; text: string }

declare module 'claude-code' {
  interface PluginState {
    'agent-hub': {
      agents: AgentRow[]
      peers: PeerRow[]
      messages: MessageRow[]
      isRouting: boolean
      routedCount: number
      peersCheckedAt: number
    }
  }
}
