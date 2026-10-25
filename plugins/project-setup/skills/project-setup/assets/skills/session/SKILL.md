---
name: session
description: Open or close a working session on this project - load the right context at the start, and at the end write the session report and update tasks, context, changelog, decisions and the roadmap. Use when the user says start/open/begin a session, end/close/wrap up a session, or asks what was done this session.
---

<!-- Template from project-setup. Tailor: the read order, the files the close
updates, and the milestone IDs in the effort line. Remove this comment. -->

# session

The docs system only works if the loop actually runs. `CLAUDE.md` describes it;
this skill executes it, because advisory guidance is the first thing dropped
when context gets tight.

Two modes. Infer from the request; ask only if genuinely ambiguous.

---

## Opening a session

1. **Read, in this order:**
   - `docs/INDEX.md`: the map
   - `docs/tasks.md`: what is active
   - `docs/roadmap.md`: which phase, and its exit criteria
   - the newest file in `docs/sessions/`: where the last session stopped
   - `docs/context/`: only the parts relevant to the work at hand

2. **Run `docs-audit`** if more than a few days have passed, or if a source of
   truth may have changed. Stale context is worse than none: it is wrong with
   confidence.

3. **Report to the user, briefly:** the phase, the active task, what blocks it,
   and anything the audit flagged. Then ask what they want to work on. Don't
   assume it is the Now item.

Don't write a session file on open. It is written at close, when there is
something to say.

---

## Closing a session

Work through all six. Skipping one silently is how the system rots.

1. **Session report**: `docs/sessions/YYYY-MM-DD-NN-slug.md` from the template
   in `docs/sessions/README.md`. Prose, not a commit log: what was tried, what
   was rejected and why. Include the effort line
   (`**Effort:** ~2h · M-NN · advanced`). Add it to the sessions index.
2. **Tasks**: move finished items to Done with the date; promote the next; one
   item in Now. Say what blocks anything blocked.
3. **Context**: only if something is now true that wasn't before. Fold answered
   questions in and move them to Answered. Strip `[unconfirmed]` once
   confirmed.
4. **Roadmap**: tick exit criteria that now hold. If a milestone completed, run
   the milestone checkpoint (audit, grill the decisions it relied on, review the
   tooling). If the schedule now looks wrong, say so.
5. **Changelog**: only if something shipped. Otherwise skip and say so.
6. **Decisions**: anything chosen over a real alternative gets a `D-NNN` with
   alternatives, consequences and **Revisit if**.

## Then

Run `docs-audit` and fix what it flags. Commit only if the owner asks, with a
message that explains the reasoning. Tell the owner in a few lines: what moved,
what's next, and anything that needs them, especially unanswered questions.
