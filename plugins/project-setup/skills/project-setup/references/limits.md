# Limits: hard rules, hooks, asking, budget

Limits say what the agent may not touch, what it can't see, when it must stop
and ask, and how much it may spend. They scale with **autonomy** and with
**what is expensive to undo**.

## Three layers

Use the weakest layer that is enough, and the strongest for anything
irreversible:

| Layer | Where | Enforced by | Use for |
|---|---|---|---|
| Rule | `CLAUDE.md` hard rules | The agent following instructions | Judgement calls: "never widen scope", "don't tick a question for the owner" |
| Deny rule | `.claude/settings.json` → `permissions.deny` | Claude Code, by command or path prefix | Paths: read-only `reference/**`, `.env*`, `secrets/**`, a live data file |
| Hook | `.claude/hooks/*.py` on `PreToolUse` | A script that inspects the whole command | Destructive commands deny rules miss (`git push origin main --force` slips past a `git push --force` prefix rule) |

A rule that matters enough to cost real damage if skipped gets a deny rule or
hook too. `CLAUDE.md` still states it, so the agent knows why it was blocked.

## By autonomy

| Autonomy | Limits to add |
|---|---|
| Owner watches | Hard rules for sources and secrets. Deny rules on read-only paths. Usually no hook |
| Owner steers | Plus: never resolve an owner's question silently (write a `Proposal:`); never change an accepted decision without a superseding one; don't move the goalposts (test targets and fixtures are owner-owned) |
| Agent unattended | Plus: the guardrail hook; definition of done; "say what's unverified"; no pushes or merges to release branches; migrations must work with the previous release; a list of what still needs the human |

## By what is expensive to undo

| Risk | Limit |
|---|---|
| Live data (a workbook, a phone, a database) | Read-only by deny rule and by tool design; never committed (`.gitignore`) |
| Secrets | Deny `Read(./.env)`, `Read(./.env.*)`, `Read(./**/.env*)`, `Read(./secrets/**)`; the hook blocks shell commands touching them; only `.env.example` is committed |
| Money | Never place real orders, trades or payments; state it in the purpose and the hard rules |
| Deploys and releases | Name the branch that deploys; the agent opens PRs to it only when asked and merges only when told in that session |
| Messages and publishing | Never send, post or publish without the owner's explicit OK in that session |
| A live server | Read-only inspection first; validate config before applying (`docker compose config --quiet`); every change reversible and logged |
| History | No force-push, `reset --hard`, `clean -f`, branch force-delete (the hook) |

## The guardrail hook

`assets/hooks/block_destructive.py` with `test_block_destructive.py`. It blocks
force-pushes and remote branch deletion, discarding uncommitted work, history
rewrites, recursive deletes outside safe folders, and any shell command
touching `.env*` or `secrets/`. Install it when the agent works unattended, or
when the owner asks for it. Ask before installing it: it changes what commands
can run.

To install:

1. Copy both files to `.claude/hooks/`.
2. Edit `SAFE_RELATIVE` for this project's build and cache folders.
3. Add the `PreToolUse` block from `assets/settings.json` to
   `.claude/settings.json`. The wrapper turns any hook failure into a block.
4. Run `python .claude/hooks/test_block_destructive.py`; all must pass.
5. In `CLAUDE.md` → Guardrails: what it blocks, and "if it blocks you, stop and
   ask the owner; don't work around it".

## Budget

From the grill's budget answer:

- **Plan limits**: run expensive sub-agents (the red team) only for one-way
  decisions; use a cheaper model for summarising sub-agents.
- **Free-tier quotas** (an API, a voice service): check usage before calling;
  never regenerate unchanged output; keep generated output with its inputs.
- **Owner attention** is a budget too: grill two-way doors lightly; batch
  questions by dependency, never all at once.

## What still needs the owner

End the limits section of `CLAUDE.md` with an explicit list. Typical entries:
changing scope, changing hard rules, deleting (not archiving) docs, accepting a
one-way decision, anything outward-facing (push, publish, send, deploy).
