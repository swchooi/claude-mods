---
name: docs-audit
description: Check the docs for drift that is mechanically checkable - docs missing from the index, broken links and heading anchors, IDs (D-NNN, Q-NNN, T-NNN, M-NN) referenced but never defined or defined twice, missing frontmatter, and snapshot docs past their stale_after date. Use after any session that changed docs, after answering questions or recording decisions, at every milestone checkpoint, as the last step of grill, when starting a session after time away, or when the user asks to audit, verify, or check the docs.
---

<!-- Template from project-setup. Tailor: the groups this project uses, any
project-specific drift (a source file's as-of date), and the conventions list.
Remove this comment. -->

# docs-audit

Docs rot silently. This skill catches the rot that's mechanically checkable, so
human attention goes to the part that isn't.

## Run it

```bash
python tools/docs_audit.py
```

| Flag | Effect |
|---|---|
| `--quiet` | hide passing checks: best for a mid-session spot check |
| `--only GROUP` | one group; repeatable |
| `--repo PATH` | audit another checkout (e.g. a worktree) |
| `--hook-exit` | exit 2 instead of 1 on FAIL, for wiring into a `Stop` hook |

Exit code is 1 on any FAIL, 0 otherwise. Configuration (what to scan, the
index mode, ID patterns, required frontmatter) is in `tools/docs_audit.json`;
without it the script's defaults apply.

## The groups

| Group | Catches |
|---|---|
| `STRUCTURE` | a doc under `docs/` not listed in the index (or its folder README), a docs folder with no README |
| `LINKS` | a relative link to a file or heading anchor that doesn't exist |
| `IDS` | an ID referenced but never defined, or defined twice; numbering gaps (WARN) |
| `FRONTMATTER` | a doc missing a required key (only if configured) |
| `STALE` | a snapshot doc past its `stale_after` date (WARN) |

## Reading the output

**FAIL** = a factual contradiction: something points at nothing, or two places
say different things. Fix the doc, or fix the reference.

**WARN** = a judgement call for a human. Never auto-"fix" a WARN into silence.
A numbering gap may be a deleted ID (fine: IDs are never reused) or a typo.

## What to do with findings

Work in this order, because earlier ones invalidate later ones:

1. **`STALE`**: re-verify the doc against the real system, update its figures
   and `verified` / `stale_after`. Don't just move the date.
2. **`IDS` duplicate or dangling**: check whether the ID was mistyped before
   editing. Deleting a real reference hides a gap. Never renumber an ID.
3. **`FRONTMATTER`**: add the missing keys.
4. **`STRUCTURE`**: usually a file added without an index entry.
5. **`LINKS`**: mechanical; safe to fix directly.

Never tick a question or change a decision's status to silence a check. Then
tell the user what changed and what you chose not to change.

## Conventions the checks rely on

- A decision is defined by its heading `### D-NNN Title`; a question by
  `- [ ] **Q-NNN** text` (`- [x]` when answered); a task by a table row starting
  `| T-NNN |`; a milestone by a row `| M-NN |` or a heading. Everywhere else an
  ID is a reference.
- IDs inside `inline code`, fenced blocks or HTML comments are ignored: use
  that for examples.
- Frontmatter is flat `key: value` lines.

## Extending it

Add a check when you find drift the audit missed: that's the signal it has a
gap. Deterministic checks go in `tools/docs_audit.py`; judgement calls belong
here as prose, not as a regex that will misfire. A check that produces false
positives is worse than no check, because it trains everyone to ignore the
output.
