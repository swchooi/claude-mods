# Instructions: CLAUDE.md, rules, project skills

Instructions tell the agent its role, scope and rules. `CLAUDE.md` is always
loaded, so it is short and points at everything else.

## CLAUDE.md

Template: `assets/CLAUDE.md`. Under ~100 lines; detail goes in `docs/` and is
linked. Sections, in this order, dropping any that would be empty:

1. **Title and one-paragraph purpose.** What this is, for whom, what it never
   does. For a one-off, this plus "Goal" is most of the file.
2. **Current phase** (if phases exist): what is allowed right now and what
   isn't yet ("no engine chosen; don't write game code until ADR-0001 is
   Accepted").
3. **Where to look**: a table of the docs a session needs, with when each
   changes, and the start-of-session reading order.
4. **Commands**: build, test, run, audit. Read-only inspection commands first
   for live systems.
5. **Rules / hard rules**: the limits from [limits.md](limits.md), each one
   line, with the reason or the decision ID.
6. **Asking the owner**: the question protocol (below).
7. **Skills and agents**: one line each on when to use them.
8. **Conventions**: dates, IDs, naming, units, Markdown style.
9. **End of session**: the closing routine from [loop.md](loop.md), or a
   pointer to the `session` skill.

Write it for the agent: imperative, specific, with the reason when a rule would
otherwise look arbitrary. Don't restate what the code or the docs already say;
link instead.

**`AGENTS.md`**: if other agents (Codex, Gemini) will work in the project too,
keep a copy at the root and say in `CLAUDE.md` which file is the source.

## The question protocol

Every project where the owner decides things gets this section. It has been
confirmed across the owner's projects:

```markdown
## Asking the owner
- One question at a time, most-blocking first.
- Every question comes with: the options, your recommendation, and one line on
  what changes depending on the answer.
- Push back once with evidence if an answer conflicts with it; then the owner's
  call stands. Record the accepted risk.
```

For an unattended agent, add the blocked protocol instead of waiting:

```markdown
- When blocked or unsure about a product decision: add a question to
  QUESTIONS.md with your recommended default, record the default as a
  `Provisional` decision, proceed where it's reversible, and move on.
```

## .claude/rules/

Use path-scoped rules when a rule applies only to part of the tree and would
bloat `CLAUDE.md` (`frontend/**` styling rules, `migrations/**` safety rules).
One topic per file. Skip for small projects.

## Project skills

A skill is worth adding when a procedure runs repeatedly and is the kind of
thing that gets skipped when context is tight. Choose from `assets/skills/`
and tailor every path and lens to this project:

| Skill | Add when | Tailor |
|---|---|---|
| `grill` (+ `lenses.md`) | One-way decisions ahead; owner steers | Step 2's ground files; project lenses (replace the examples); where verdicts are recorded (D-log or ADR) |
| `docs-audit` | The docs audit script (`assets/tools/docs_audit.py`) is installed | `tools/docs_audit.json` (index mode, ID patterns, required frontmatter); project-specific drift (a source file's as-of date). Its `STALE` group covers snapshot docs with `stale_after` |
| `session` | Owner steers and sessions are long | The read order; which files the close updates; the effort line's milestone IDs |

Not every project needs skills. A one-off has none; a learning project's
"lesson created" routine fits in `CLAUDE.md`.

## Writing a new project skill

When the grill turns up a recurring procedure the assets don't cover, write it
in the same shape: frontmatter `name` and a `description` that says what it
does **and when to use it** (trigger phrases); a one-paragraph reason it exists;
numbered steps; a Rules section. Keep it under ~300 lines; move detail into a
reference file beside it.
