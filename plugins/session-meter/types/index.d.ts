export type Limit = { label: string; percentUsed: number; resetsAt?: string }

export type Meter = {
  ctxTokens?: number
  window: number
  // % of room left before auto-compact; null when auto-compact is off
  compactLeft?: number | null
  limits: Limit[]
  // session cost converted to MYR at an estimated rate
  costMyr?: number
}

declare module 'claude-code' {
  interface PluginState {
    'session-meter': { meter: Meter | null }
  }
}
