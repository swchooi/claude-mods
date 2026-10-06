# claude-mods

A Claude Code plugin marketplace with one plugin:

- **session-meter**: a coloured band above the prompt showing context tokens, room left before
  auto-compact, 5-hour and 7-day usage limits with reset times, and session cost.

## Install

```bash
claude plugin marketplace add swchooi/claude-mods
claude plugin install session-meter@chooi-mods
```

Start a new session, in the terminal or the desktop app's Code tab, and the band appears after the first reply.

## Update / remove

```bash
claude plugin marketplace update chooi-mods
claude plugin update session-meter@chooi-mods
claude plugin uninstall session-meter@chooi-mods
```
