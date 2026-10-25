# The loop: sessions, done, checkpoints

The docs only work if the loop runs: each session reads the right things at the
start and writes the right things at the end. Advisory guidance is the first
thing dropped when context gets tight, so make the loop short and explicit.

## Start of a session

Pick by autonomy; write the chosen one into `CLAUDE.md`:

| Autonomy | Read at start |
|---|---|
| Owner watches | `CLAUDE.md` only, or the index if there is one |
| Owner steers | `docs/INDEX.md` → `tasks` (Now) → roadmap phase → newest session report → only the `context/` parts the task touches. Say if the docs look out of date against the files |
| Agent unattended | Top entry of `handoff.md` → roadmap **Now** → `QUESTIONS.md` for newly answered questions (act on them) → the architecture part and gotchas for the area. Search decisions before reopening a choice |

Then report briefly (phase, active task, blockers) and ask what to work on.
Don't assume it is the Now item.

## End of a session

| Autonomy | Write at end |
|---|---|
| Owner watches | Update `CLAUDE.md` if a rule or limit changed |
| Owner steers | Session report (request, what was done and why, what was rejected, open issues) → tasks → `context/` if the world changed → changelog if something shipped → decisions → roadmap if a milestone moved → docs audit |
| Agent unattended | `handoff.md` entry at the top → roadmap status → promote durable lessons to gotchas → docs committed with the work they describe |

For an owner-steered project with long sessions, install the `session` skill:
it runs both routines so they aren't skipped.

## Definition of done

Write one into `CLAUDE.md` for anything that produces code or deliverables.
Draw from:

- tests and lint pass; new behaviour has tests
- UI changes checked in a browser (light and dark, desktop and phone width)
- the matching docs updated in the same change
- the commit message says what changed and why
- anything that couldn't be verified is said, not claimed

## Checkpoints

For projects with milestones: at each milestone, audit the docs, grill the
decisions the milestone relied on against their **Revisit if** triggers, and
review the tooling (add what the next milestone needs, remove what went unused).
Write it into the roadmap so it isn't skipped.

## Conventions worth fixing early

- Session reports: `docs/sessions/YYYY-MM-DD-NN-slug.md`, `NN` from `01` each
  day; prose, not a commit log; append-only.
- Handoff: newest first, ~10 entries, older ones archived after durable lessons
  moved to gotchas.
- Effort line (optional, for projects whose schedule is a guess):
  `**Effort:** ~2h · M-05 · advanced`.
