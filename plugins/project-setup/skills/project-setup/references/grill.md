# Purpose grill

The interview that finds out what the project is, so the structure can follow
from it. It is not the decision `grill` (which tests a proposal); it builds the
**project profile** that every other part is chosen from.

## How to ask

- **One question at a time.** Wait for the answer; it may settle later ones.
- **Every question comes with**: the options, **your recommendation**, and one
  line on what changes depending on the answer.

  > **Who will do most of the work?**
  > 1. You, watching each session (recommended: it's a two-week tool)
  > 2. You steer; Claude works between check-ins
  > 3. An agent works unattended; you review results
  >
  > *Changes:* 2 adds a questions file and session reports; 3 adds a handoff
  > log, provisional decisions and stricter guardrails.

- Use the question tool when the options are discrete; prose when the answer is
  something only the owner knows ("what does the workbook track?").
- **Answer from the files first.** If the folder already says it, state what
  you found and move on.
- **Push back once** if an answer conflicts with the evidence. Then the owner's
  call stands.
- **Stop** when the next answer would not change the structure.

## The questions

In order. Skip any that earlier answers or the files settle. The **Drives**
column says which parts the answer changes; if it would change nothing for this
project, skip it.

| # | Question | Typical options | Drives |
|---|---|---|---|
| 1 | **What is this, in one sentence?** What problem does it solve, for whom? | free text | Everything; `context/purpose` or `product.md` |
| 2 | **What does done look like?** How will you know it worked? | a deliverable · a working app · a habit/ongoing service · learning | Loop (definition of done), roadmap or not |
| 3 | **How long will it live?** | days (one-off) · weeks · months · ongoing | Memory size; whether decisions/sessions exist at all |
| 4 | **Who does the work?** | owner watches · owner steers, Claude works between · agent unattended | Limits, loop (handoff vs session reports), questions file |
| 5 | **What kind of project is it?** | see [archetypes](#archetypes) | The starting structure |
| 6 | **What are the sources of truth, and which are read-only?** A workbook, a server, a client's spec, a reference image, a live database | free text, per source | Limits (deny rules), `reference/`, tools (dumpers, mirrors) |
| 7 | **What is sensitive?** Money, personal data, credentials, files that must not leave the machine | none · private data · secrets · money moves | Limits, `.gitignore`, whether a remote is allowed |
| 8 | **What would be expensive to undo?** | nothing much · schema/stack choices · real-world actions (deploys, payments, messages) | Decision log type (light D-log vs ADRs), `grill` + `red-team`, hooks |
| 9 | **What does it produce?** | code · documents/artifacts · lessons · reports · a model/drawing | Folder layout (`artifacts/`, topic folders, `src/`) |
| 10 | **What tools or systems does it touch?** MCP servers, APIs, a server over SSH, a desktop app, a browser | free text | Tools: `.mcp.json`, scripts, allowlist |
| 11 | **How often will you work on it, and how much attention can you give?** | daily · weekly · in bursts | Question format, how much the agent may decide alone, checkpoint cadence |
| 12 | **Version control?** | none · local git · private GitHub · public GitHub; large binaries? | [version-control.md](version-control.md) |
| 13 | **Budget?** Plan limits, API costs, free-tier quotas (ElevenLabs, a data API) | free text | Limits (budget rules); whether expensive sub-agents run |
| 14 | **Conventions?** Language, units, currency, time zone, naming | defaults from the owner's other projects | `CLAUDE.md` conventions |

Questions 1–5 are always asked (or answered from files). 6–14 only when they
would change something.

**Follow-ups worth one more question:** a "months" lifespan with no done-when
("what would make you stop?"); "unattended" with real-world actions ("which of
these must always wait for you?"); "read-only" sources the agent must read
often ("should there be a tool that dumps it?").

## Archetypes

The closest one is the starting point; the answers then add or drop modules.
Examples are the owner's own projects, which show each shape working.

| Archetype | Looks like | Memory | Instructions and limits | Example |
|---|---|---|---|---|
| **One-off tool** | days–weeks, owner watches, one clear deliverable | `CLAUDE.md` only (goal, hard rules, shorthands, how it works, known limits); a `GUIDE.md` if someone will rerun it | Hard rules inline; enforce read-only in code if it touches devices or live data | phonediff |
| **Learning / content** | ongoing, owner learns, output is lessons or pages | `docs/index.md` tracker + one `README.md` progress log per topic folder | Teaching or writing style section; publish steps | learn |
| **Steered product** | months, owner steers, one-way decisions ahead | `context/` (present tense), decisions with **Revisit if**, questions, roadmap with milestones, session reports, tasks, glossary | `grill`, `docs-audit`, `session` skills; `red-team` agent; question protocol | spendingrecords, driving-game |
| **Autonomous product** | months, agent works unattended, owner reviews | `product.md`, `architecture/`, `design/`, append-only decisions (with `Provisional`), roadmap, newest-first `handoff.md`, `QUESTIONS.md` at the root, structure-change triggers | Definition of done, "when blocked" protocol, hard rules on money/secrets/releases, guardrail hook | investiapp |
| **Ops / infrastructure** | ongoing, touches a live system | Architecture, runbooks, baselines and reports with `verified` / `stale_after` / `watch`, changelog, tasks | Safety rules, read-only inspection commands first, `stale-audit`; validate before deploy | kittyserver |
| **Workspace / hub** | ongoing, spans other projects | `context/` (purpose, registry, conventions, environment), decisions, questions, tasks, changelog, sessions; dated `artifacts/`; `tools/` | Start and end routine; where outputs go | general |
| **Design / reference** | weeks–months, works on a model or drawings through a tool | `reference/` (read-only, every file's source and date in its README), `exports/`, a decisions list | MCP setup; units and conventions; what may be edited in the model | Revit |

Hybrids are normal: a steered product that also deploys to a server takes the
ops module for its deploy docs.

## The profile

Write it as a short block, kept in the conversation for step 3 and copied into
the first decision record:

```markdown
**Project profile** (YYYY-MM-DD)
- Purpose: …
- Done when: …
- Lifespan: … · Autonomy: … · Archetype: … (+ modules)
- Sources of truth: … (read-only: …)
- Sensitive: … · Expensive to undo: …
- Produces: … · Touches: …
- Cadence and attention: …
- Version control: … · Budget: …
- Conventions: …
```

## Mapping answers to parts

| Answer | Adds |
|---|---|
| Lifespan ≥ months | Decisions log, session reports or handoff, tasks |
| Owner steers | Questions with options + recommendation, `grill` skill, session reports |
| Agent unattended | `handoff.md`, `QUESTIONS.md` at root, `Provisional` decisions, definition of done, guardrail hook |
| Read-only source | Deny rules on its path, `reference/` README with provenance, a dump/inspect tool |
| Sensitive data | `.gitignore` entries before first commit, deny rules on `.env*`/`secrets/`, no remote or private only |
| One-way decisions | Decisions with **Revisit if**; ADRs if there will be many; `red-team` agent |
| Real-world actions | Hard rules naming each action and who may trigger it; hook if a command can do it |
| Live system | Read-only inspection commands listed first; snapshot docs with `stale_after` |
| Several docs or IDs | `docs/INDEX.md` or per-folder READMEs, and the docs audit |
| Free-tier or plan budget | Budget rules in `CLAUDE.md`; expensive sub-agents only for one-way doors |
