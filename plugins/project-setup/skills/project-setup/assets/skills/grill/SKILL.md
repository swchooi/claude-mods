---
name: grill
description: Stress-test a proposal, plan or design before it becomes a decision, or brainstorm options for an open question, by interrogating it against the project's purpose, its real data and its existing decisions, then interviewing the owner one question at a time. Use when the user says grill, stress-test, challenge, poke holes, red-team, pre-mortem, brainstorm, or asks whether a plan/proposal/design is sound; before recording any decision that would be expensive to reverse; and at every milestone checkpoint.
---

<!-- Template from project-setup. Tailor: step 2's ground files, step 1's door
examples, step 7's record locations, and the project lenses in lenses.md.
Remove this comment. -->

# grill

A proposal that has only been read by its author has not been reviewed. This
skill turns "does this look right?" into a procedure: generate alternatives,
attack the proposal from named angles, answer from the files what can be
answered, ask the owner the rest one question at a time, and write the verdict
into the docs.

It is **not** devil's advocacy for its own sake. Every challenge must be
concrete, and the session ends when answers stop changing the plan.

Three modes, inferred from the request:

- **Grill**: a proposal exists. Test it.
- **Diverge**: only an open question exists. Generate options first (step 3),
  then grill the favourite.
- **Checkpoint**: a milestone just closed. Grill the decisions it relied on
  against their **Revisit if** triggers.

---

## 1 · Frame

Write down, before anything else:

- **The decision**, in one sentence. If it won't fit in one, it is several
  decisions. Split them and grill each, in dependency order.
- **What reversing it would cost later.** This sets the depth:

| Door | Examples | Depth |
|---|---|---|
| **One-way**: reversing means a migration, a rewrite, or redoing content | <this project's: schema, stack, data format, …> | Full: every step, plus the independent red team (4b) |
| **Two-way**: changeable in an afternoon | <a default, a label, a layout, a tuning value> | Light: steps 1, 4 (two or three lenses), 6. About five minutes |

Grilling a two-way door at full depth wastes the owner's attention, which is the
scarcest resource in the project.

## 2 · Ground: answer from the evidence before asking

Read what the proposal touches:

- `<decisions file>`: what it must stay consistent with
- `<purpose / vision doc>`: goals, principles, non-goals
- `<source-of-truth doc>`: what the data or system actually does
- `<questions file>`: whether this is already an open question

**Anything the files, the data or a quick experiment can answer, answer
yourself. Don't ask the owner.** Where a proposal makes a checkable claim
("every X is Y", "the library supports Z"), check it and report what you found,
with a count where there is one. One real counter-example outweighs any amount
of argument.

## 3 · Diverge

If fewer than three options are on the table, generate them:

- **Don't do it**: the status quo, or the simplest thing that could work
- **The obvious one**: usually the proposal
- **The bold one**: what it would look like if a constraint everyone assumes
  were removed

**Steelman each one before criticising any of them.** An option that can't be
steelmanned was never really an option. Drop it and say why.

## 4 · Attack

### 4a · Lenses

Pick the lenses that bite from [`lenses.md`](lenses.md). Usually 3–6, never all
of them. Always include **consistency** for a one-way door. For each lens,
produce a **finding**, not a question:

> **Pre-mortem.** It is <a date a year out> and <the goal> failed. Cause: <a
> specific chain of events ending in a specific symptom>.

A finding names a scenario, a number, a document, or a decision it collides
with. "Have you considered edge cases?" is not a finding. Delete it.

Classify each finding:

- **Fatal**: the proposal can't stand as written
- **Amend**: it survives with a specific change. Name the change.
- **Accept the risk**: real, but cheaper to live with. Say why.
- **Needs data**: undecidable without an answer from the owner or an
  experiment. This becomes a question in step 5.

### 4b · Independent red team (one-way doors only)

The author of a proposal is the worst-placed reviewer of it, and that author is
usually the assistant running this skill. For a one-way door, start the
**`red-team` agent** in the background. Give it only:

- the path to the proposal
- what is being decided

**Don't** pass it your reasoning, your findings, or the conversation. Do your
own step 4a while it runs. Then merge its findings with yours, and **report
which findings only the red team found.** That number measures how much your
own review missed.

Skip this for two-way doors. It costs a full agent run.

## 5 · Interrogate the owner

Only for the **needs-data** findings, and for any fatal or amend finding where
the fix is the owner's call.

- **One question at a time.** Wait for the answer.
- **Dependency order.** Ask the question that unblocks most of the others first.
- **Every question comes with**: the options, **your recommendation**, and one
  line on what changes depending on the answer.
- Use the question tool when the options are discrete; prose when the answer is
  something only the owner knows.
- **Push back once** on an answer that conflicts with the evidence, citing the
  evidence. If the owner holds, their call stands. Record the accepted risk.
- **Stop** when the next question wouldn't change any verdict.

## 6 · Verdict

One line per proposal:

| Verdict | Meaning |
|---|---|
| **Accept** | stands as written |
| **Amend** | stands with the named changes |
| **Reject** | the alternative that replaces it, and why |
| **Needs data** | what data, from whom, and what's blocked until then |

Each accepted or amended decision also gets a **Revisit if**: the concrete
observation that would reopen it. A decision with no revisit trigger is being
treated as permanent, and almost none are.

## 7 · Record

Only after the owner has given the verdict their OK:

- Accepted and amended proposals → `<decisions file>`, a new entry each,
  including **Revisit if**.
- The documents the proposal lives in: apply the amendments and strip any
  "draft" or `[unconfirmed]` status from what was accepted.
- New questions → `<questions file>`.
- The session report or handoff gets a **Grill** section: lenses used, what the
  red team found that the author missed, which findings changed the plan, which
  risks the owner accepted.
- Then run `docs-audit` if the project has it.

Finish by telling the owner in a few lines: the verdicts, which findings changed
the plan, what the red team found that you missed, and which risks they
accepted.

---

## Rules

- **Concrete or cut.** Every finding names a number, a scenario, a document or a
  decision.
- **Past decisions aren't reopened without new evidence.** New evidence reopens
  them properly: a superseding decision, never a quiet edit.
- **No false balance.** If one option is simply better, say so.
- **State your confidence** on each finding: verified, owner-stated, or
  inferred.
- **The owner decides.** This skill makes the owner's decision better informed.
  It never makes it for them.
