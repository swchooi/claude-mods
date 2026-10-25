# Memory: the docs/ structure

Sessions don't remember each other. The docs are the project's memory: anything
a later session needs (what this is, how it works now, what was decided, what is
next, what just happened) lives here or is lost.

## Principles that hold for every size

- **Each file has a contract**: the question it answers, its shape, and when it
  changes. Write the contract down in `docs/README.md` as a table. This is what
  keeps a later session from putting things in the wrong place.

  | File | Answers | Shape | Changes when |
  |---|---|---|---|

- **Tense separates files.** `context/` (or `architecture.md`) is the present
  tense, edited in place; stale content is a bug. Sessions, handoffs and the
  changelog are the past, append-only. Decisions are the reasoning. The roadmap
  is the future. "As of last week…" in a present-tense file belongs in a
  session report.
- **One owner per fact.** Each fact is defined in one file; others link to it.
  A short restatement with a link is fine where a reader needs it (`CLAUDE.md`
  repeats hard rules because it is always loaded).
- **IDs are never renumbered or reused.** Prefixes per kind (`D-001`, `Q-001`,
  `T-001`, `M-01`, `ADR-0001`). Write the prefix table in the index if there are
  more than two kinds, and call out look-alikes.
- **Absolute dates**, YYYY-MM-DD, with the owner's time zone stated once.
- **Say what is unverified.** Mark inferred claims `[unconfirmed]` until checked.
- **`docs/` is tool-neutral**: usable by a human or any agent. Agent-specific
  instructions go in `CLAUDE.md`.

## Modules

Pick by the profile. Each row says when it earns its place and its default
location.

| Module | Earns its place when | Default file(s) | Shape |
|---|---|---|---|
| Index | More than ~6 docs, or IDs in use | `docs/INDEX.md` (or a `README.md` per folder listing its docs) | Map of every file and ID range |
| Docs contract | Any `docs/` folder | `docs/README.md` | The contract table, start/end routine, upkeep rules |
| Purpose / product | Always, except one-offs (where it's `CLAUDE.md`'s first section) | `docs/context/purpose.md` or `docs/product.md` | Goal, for whom, non-goals, done-when. Changes only when the owner changes scope |
| Present state | Anything with a design or system | `docs/context/*.md` or `docs/architecture.md` (+ `architecture/`) | Rewritten in place |
| Source model | A source of truth that needs explaining (a workbook, an API, a building) | `docs/context/<source>-model.md` | What it does, with counts and as-of date |
| Feature design | Exact rules a feature must follow | `docs/design/<topic>.md` | Written before the code, kept current with it |
| Decisions | Lifespan ≥ months, or any one-way door | `docs/decisions.md` (D-NNN table) or `docs/adr/NNNN-*.md` | Append-only; status line is the only in-place edit; **Revisit if** on every accepted one |
| Questions | Owner steers or agent works unattended | `docs/questions.md`, or `QUESTIONS.md` at the root when an agent works unattended (it's the one file the owner checks) | Open / answered; each answer points to where it was recorded |
| Roadmap | Phases or milestones exist | `docs/roadmap.md` | Now / next / later, milestones with exit criteria |
| Tasks | More than a handful of work items, no issue tracker | `docs/tasks.md` (or `tasks/current.md` + `backlog.md`) | One item in Now |
| Session reports | Owner steers, sessions are long | `docs/sessions/YYYY-MM-DD-NN-slug.md` | Append-only prose: request, what was done and why, what was rejected, open issues |
| Handoff | Agent works unattended | `docs/handoff.md` | Newest first, keep ~10, archive older; durable lessons promoted to gotchas |
| Gotchas | Code exists | `docs/architecture/gotchas.md` | Durable lessons that cost time, by topic |
| Changelog | Something ships to users or a server | `docs/changelog.md` | Dated, newest first |
| Glossary | Domain vocabulary the owner uses | `docs/glossary.md` | Living |
| Runbooks / baselines | Ops on a live system | `docs/runbooks/`, `docs/baselines/` | Snapshot docs carry `verified`, `stale_after`, `watch` frontmatter |
| Reference | Read-only source material | `reference/` (outside `docs/`) with a README giving each file's source and date | Never edited |
| Reviews | Independent reviews of one-way decisions | `reviews/YYYY-MM-DD-slug.md` (outside `docs/` so reviewers stay independent) | Snapshot |
| Artifacts | Deliverables that get rebuilt | `artifacts/YYYY-MM-DD-slug/` with README (what, how made, how to update) | Outputs plus everything needed to rebuild; intermediates git-ignored |
| Topic folders | Learning or content | `<topic>/README.md` + one file per lesson | Progress log per topic |

## Growth triggers

Write these into `docs/README.md` under "Changing the docs structure", so the
structure grows by rule instead of by guesswork. Only list triggers for modules
that were left out or will need splitting. Examples:

| Change | Trigger |
|---|---|
| Split `architecture.md` into `architecture/` | It passes ~400 lines |
| Add `adr/` with a template | The first one-way decision |
| Add `design/<topic>.md` | Before building a feature whose rules need exact definitions |
| Archive old handoff entries to `archive/handoff-YYYY.md` | More than 10 entries |
| Archive superseded decisions | More than ~50 entries; keep the full index |
| Add `glossary.md` | The third time a term needs explaining |
| Add the docs audit | IDs or cross-links exceed what a reader checks by eye (~10 docs) |

Also write who may restructure: by default the agent may create, split and
archive per these triggers and must mention it in the session report or
handoff; **deleting** content and changing scope need the owner.

## Frontmatter

Optional. Worth it when the docs audit checks it, or when snapshot docs need
staleness fields. Keep it flat (`key: value`):

```yaml
---
type: Context | Decision | Design | Runbook | Baseline | Review
title: …
description: one line; the folder index carries it verbatim
status: Draft | Current | Snapshot
updated: YYYY-MM-DD
# snapshot docs only:
verified: YYYY-MM-DD
stale_after: YYYY-MM-DD
watch: what change would make this wrong
---
```

## Templates

`assets/docs/`: `README.md` (contract table and routines), `INDEX.md`,
`decisions.md`, `questions.md`, `handoff.md`, `session-report.md`. Fill them
from the grill; delete sections that don't apply.
