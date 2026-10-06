import type { Engine, Register, SessionContextUsage, SessionRateLimit, SessionCost } from 'claude-code'

import type { Limit, Meter } from '../types'

type Figures = { context: SessionContextUsage; rateLimits: SessionRateLimit[]; cost?: SessionCost }

const meter = { plugin: 'session-meter', key: 'meter' } as const

const GREEN = 'green'
const AMBER = 'yellow'
const RED = 'red'

// Colour for a % used: green, amber from 70, red from 90.
const usedColor = (pct: number) => (pct >= 90 ? RED : pct >= 70 ? AMBER : GREEN)

// Colour for a % of room left: red at 10 or under, amber at 25 or under.
const leftColor = (pct: number) => (pct <= 10 ? RED : pct <= 25 ? AMBER : GREEN)

const trim = (s: string) => s.replace(/\.0$/, '')

const k = (n: number) =>
  n >= 1_000_000 ? `${trim((n / 1_000_000).toFixed(1))}M` : n >= 1000 ? `${trim((n / 1000).toFixed(1))}k` : `${n}`

// One coarse unit only: "40m", "4h", "2d".
const resetsIn = (iso: string | undefined, now: number) => {
  const at = iso ? Date.parse(iso) : NaN
  if (!Number.isFinite(at) || !Number.isFinite(now)) return ''
  const mins = Math.max(0, (at - now) / 60000)
  const span = mins < 60 ? `${Math.round(mins)}m` : mins < 1440 ? `${Math.round(mins / 60)}h` : `${Math.round(mins / 1440)}d`
  return ` resets in ${span}`
}

async function measure($: Engine, f: Figures): Promise<Meter> {
  const { tokens, window } = f.context
  let compactLeft: number | null | undefined

  try {
    const b = (await $.session.usage({ breakdown: 'summary' })).context.breakdown
    if (b && !b.isAutoCompactEnabled) compactLeft = null
    else if (b?.autoCompactThreshold && tokens !== undefined)
      compactLeft = Math.max(0, Math.round((1 - tokens / b.autoCompactThreshold) * 100))
  } catch {
    // breakdown unavailable: leave the auto-compact figure out
  }

  const byKind = (kind: string, label: string): Limit[] => {
    const r = f.rateLimits.find(l => l.kind === kind)
    return r ? [{ label, percentUsed: r.percentUsed, resetsAt: r.resetsAt }] : []
  }

  return {
    ctxTokens: tokens,
    window,
    compactLeft,
    limits: [...byKind('five_hour', '5h'), ...byKind('seven_day', '7d')],
    costUsd: f.cost?.usd,
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const r = await next(e)
    $.ui.status(undefined)
    await $.state.set(meter, await measure($, await $.session.usage()))
    return r
  })

  on('session.measure', async ($, e, next) => {
    await $.state.set(meter, await measure($, e))
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const { value: m } = await $.state.get(meter)
    if (e.props.hasSurvey || !m) return next(e)

    const { Box, Text } = $.ui.resolve(e)
    const now = await $.clock.now()
    const sep = <Text dimColor>{'  │  '}</Text>

    return (
      <Box>
        <Text wrap="truncate">
          <Text dimColor>ctx </Text>
          <Text>{m.ctxTokens === undefined ? '–' : k(m.ctxTokens)}</Text>
          <Text dimColor>/{k(m.window)}</Text>
          {m.compactLeft === null ? (
            <Text>
              {sep}
              <Text dimColor>auto-compact off</Text>
            </Text>
          ) : m.compactLeft !== undefined ? (
            <Text>
              {sep}
              <Text color={leftColor(m.compactLeft)} bold>
                {m.compactLeft}%
              </Text>
              <Text dimColor> until compact</Text>
            </Text>
          ) : null}
          {m.limits.map(l => (
            <Text key={l.label}>
              {sep}
              <Text dimColor>{l.label} </Text>
              <Text color={usedColor(l.percentUsed)} bold>
                {Math.round(l.percentUsed)}%
              </Text>
              <Text dimColor>{resetsIn(l.resetsAt, now)}</Text>
            </Text>
          ))}
          {m.costUsd !== undefined ? (
            <Text>
              {sep}
              <Text>${m.costUsd.toFixed(2)}</Text>
            </Text>
          ) : null}
        </Text>
      </Box>
    )
  })
}
