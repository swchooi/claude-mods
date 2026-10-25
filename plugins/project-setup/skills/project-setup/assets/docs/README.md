<!-- Template for project-setup: keep only the rows for files this project has. Remove this comment. -->
# Project docs

These docs are the project's memory. Sessions remember nothing between runs, so
anything a later session needs to know (what we're building, how it works now,
what was decided, what's next, what just happened) lives here or it is lost.

## The files

| File | Answers | Shape | Changes when |
|---|---|---|---|
| [`INDEX.md`](INDEX.md) | Where is everything, and which IDs exist? | Living map | A file or ID range is added |
| [`context/purpose.md`](context/purpose.md) | What are we building, for whom, what's out of scope, what is done? | Living, short | The owner changes scope |
| [`context/…`](context/) | How do things stand right now? | Present tense, edited in place | The world changes |
| [`decisions.md`](decisions.md) | Why is it like this? | **Append-only** | A real choice between alternatives is made, or the owner answers a question |
| [`questions.md`](questions.md) | What does the owner need to decide? | Open / answered | Someone is blocked or unsure, or the owner answers |
| [`roadmap.md`](roadmap.md) | What's done, in progress and next? | Living | A milestone starts, finishes, is blocked or changes scope |
| [`tasks.md`](tasks.md) | What are we doing right now? | Now / next / later | Work starts or finishes |
| [`sessions/`](sessions/) | What happened on day X, and why? | **Append-only**, one file per session | Every session ends |
| [`handoff.md`](handoff.md) | What did the last session do, where did it stop, what bit it? | Newest first, ~10 entries | Every session ends |
| [`changelog.md`](changelog.md) | What shipped, and when? | Newest first | Something ships |

The distinction that matters: **the roadmap is the future, `context/` is the
present, sessions and the changelog are the past, decisions are the
reasoning.** If you find yourself writing "as of last week…" in `context/`, it
belongs in a session report.

## Start of a session

1. <…>

## End of a session

1. <…>

## Upkeep rules

- **Docs are part of done.** A change to behaviour, structure or a contract
  without the matching doc update is not done.
- **One owner per fact.** Each fact is defined in one doc; the others link to
  it. A short restatement with a link is fine where a reader needs it.
- **Present tense describes the present.** Rewrite outdated sections rather
  than appending "update:" notes; history belongs in decisions and git.
- **Decisions are append-only.** The only in-place edit is the **Status** line
  (`Superseded by D-015`). To change a decision, append one that supersedes it.
- **IDs are never renumbered or reused.**
- **Say what's unverified.** Label assumptions `[unconfirmed]` until checked.
- **`docs/` is tool-neutral.** Agent-specific instructions go in `CLAUDE.md`.

## Changing the docs structure

The agent may create, split and archive docs when a trigger below fires, and
mentions every structural change in <the session report / handoff>. Deleting
content outright, or changing scope, needs the owner.

| Change | Trigger |
|---|---|
| <…> | <…> |

**How to add a doc:** prefer a new section in an existing doc. A new file gets
a row in **The files** above with its update trigger, and a line in `INDEX.md`.
If sessions need it at the start, add it to `CLAUDE.md`'s "Where to look".
