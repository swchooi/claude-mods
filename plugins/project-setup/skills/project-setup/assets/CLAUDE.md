<!-- project-setup: fill every section from the purpose grill; delete any
section that would be empty. Keep the result under ~100 lines; link to docs/
for detail. Remove every "project-setup:" comment once done. -->
# <Project name>

<One paragraph: what this is, for whom, and what it never does. Full scope: `docs/<purpose or product>.md`.>

## Current phase: <M-00 — name>
<!-- project-setup: only if the project has phases. What is allowed now, and what isn't yet. -->
- <Work right now is …>
- <Don't … until …>

## Where to look

Sessions don't remember each other; these docs are the project's memory.
**At the start of every session** read <the start routine from loop.md>.

| Doc | What it holds | Update when |
|---|---|---|
| `docs/README.md` | The docs system: every file's contract, upkeep rules | The structure changes |
| `<doc>` | <…> | <…> |

## Commands

```bash
<read-only inspection commands first, then build / test / run>
python tools/docs_audit.py --quiet   # after changing docs; fix FAILs before finishing
```

## Hard rules
<!-- project-setup: from limits.md. One line each, with the reason or the decision ID. -->
- **<Source> is read-only.** <Why. Enforced by deny rule / tool.>
- **Never commit <private data> or secrets.** (`.gitignore`, D-00N)
- <…>

Still needs the owner: <changing scope, changing these rules, deleting docs, accepting a one-way decision, push / publish / deploy>.

## Asking the owner
- One question at a time, most-blocking first.
- Every question comes with: the options, your recommendation, and one line on what changes depending on the answer.
- Push back once with evidence if an answer conflicts with it; then the owner's call stands. Record the accepted risk.
<!-- project-setup: unattended agent? Replace with the QUESTIONS.md + Provisional decision protocol. -->

## Skills and agents
- **`<skill>`** — <when to use it>.

## Guardrails
<!-- project-setup: only if the hook is installed. -->
- `.claude/hooks/block_destructive.py` blocks force-pushes, discarding uncommitted work, history rewrites, recursive deletes outside <safe folders>, and shell commands touching `.env*` or `secrets/`. If it blocks you, stop and ask the owner; don't work around it. Tests: `python .claude/hooks/test_block_destructive.py`.

## Definition of done
<!-- project-setup: projects that produce code or deliverables. From loop.md. -->
- <tests and lint pass; …; docs updated in the same change; unverified things said, not claimed>

## Conventions
- Dates are absolute (YYYY-MM-DD), <time zone>.
- IDs: <D-NNN decisions, Q-NNN questions, …>. Assigned in order, never reused or renumbered.
- Version control: <local git on `main`, no remote | private GitHub `<owner>/<name>`>. Commit only when the owner asks, one commit per logical change, message says what and why. Never add a remote or push without asking.

## End of a session
<!-- project-setup: from loop.md, or: "Run the `session` skill." -->
1. <…>
