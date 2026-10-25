# Lenses

Angles of attack for `grill` step 4. Pick the ones that bite; a lens that
produces nothing concrete is dropped, not padded.

Each has the question it asks, when it earns its place, and what a real finding
looks like.

---

## General

### Pre-mortem
*"It's a year from now and this failed. What happened?"* State the failure as
certain, then explain it. Imagining the failure as already happened surfaces
causes that "what could go wrong?" doesn't (prospective hindsight).
**Use for:** every one-way door.
**Finding looks like:** a specific causal chain ending in a specific symptom.

### Inversion
*"What would guarantee this fails?"* Then check that the proposal doesn't do any
of it.
**Use for:** plans with many moving parts, where failure modes are easier to
list than success conditions.

### Assumption audit
List every assumption the proposal needs to be true. Tag each: **verified**
(tested or documented, with the source) · **owner-stated** (cite the question
or decision) · **inferred** (nobody has checked).
**Use for:** always, for one-way doors. Inferred assumptions under a one-way
door are the main output of a grill.

### Second-order effects
*"And then what?"* What does this force downstream?
**Use for:** schema, format and architecture choices.

### Reversal cost
*"If we change our mind in three months, what has to change?"* Count it: files,
tables, records, tests, screens.
**Use for:** confirming the door type from step 1. It is often wrong on first
guess.

### Counter-example hunt
*"Find one real case this doesn't handle."* Search the real data first, then
plausible near-future cases.
**Use for:** any claim of the form "every X is Y".

### Steelman the rejected
Make the strongest case for the alternative the proposal rejected. If it now
looks better, say so.
**Use for:** proposals that arrived with alternatives dismissed in one line.

### Simplest version
*"What is the smallest version of this that would still work?"* Anything beyond
it must justify itself.
**Use for:** anything that adds an entity, a field, a state or a dependency.

### Consistency
*"Does this contradict an accepted decision, a glossary term, or a documented
fact?"* Cite the decision ID.
**Use for:** every one-way door. Mandatory.

### Operational burden
*"Who runs this at 2 a.m. when it breaks?"* Upgrades, backups, monitoring,
renewals.
**Use for:** stack, hosting, sync, deployment and backup choices.

### Privacy
*"Does any private data leave where it should stay: to a service, a log, a URL,
a commit?"*
**Use for:** integrations, telemetry, error reporting, version control.

---

## This project

<!-- project-setup: replace with 3–6 lenses built from this project's principles, hard rules and
riskiest assumptions. Each one cites the decision or doc it protects. Shape:

### <Name> (`D-NNN`)
*"<The question it asks>"*
**Use for:** <which proposals>.

Examples from other projects: "Both bases: does this compute on accrual and cash
alike?" (a finance app); "Feel: can a streamer tell this happened without
reading the HUD?" (a game); "Parity: can last year's workbook still be
reproduced to the cent?" (a migration). -->
