---
name: project-setup
description: Set up a new project so Claude Code can work in it well - interview the owner about the project's purpose (the purpose grill), then generate the parts its agent needs, sized to the project - instructions (CLAUDE.md, rules, project skills), memory (the docs/ context structure), tools (MCP, scripts, permissions), limits (hard rules, hooks, when to ask), sub-agents, the session loop, and version control (git, optional GitHub). Use when the user starts a new project, asks to set up or scaffold a project's context, docs, CLAUDE.md or Claude setup, or asks to retrofit one onto an existing folder that has none.
---

# project-setup

Inside a project, Claude Code is an agent: a model with **instructions, tools,
memory and limits**, working in a **loop** toward a goal. This skill builds
those parts for one project, and only the parts the project needs. A one-off
script gets a single `CLAUDE.md`; a multi-month product gets a docs system,
decision log, review skills and guardrail hooks.

The structure follows from the purpose, so the skill starts by finding out the
purpose. **Do not generate anything before the grill is done.**

## The parts

| Part | What it is in a project | Reference |
|---|---|---|
| Purpose | What the project is for and what "done" means. Every other part follows from it | [grill.md](references/grill.md) |
| Memory | The `docs/` context structure: what is true now, what was decided, what is next, what happened | [memory.md](references/memory.md) |
| Instructions | `CLAUDE.md`, `.claude/rules/`, project skills | [instructions.md](references/instructions.md) |
| Tools | MCP servers, scripts in `tools/`, the permission allowlist | [tools.md](references/tools.md) |
| Limits | Hard rules, deny rules, hooks, when to ask the owner, budget | [limits.md](references/limits.md) |
| Sub-agents | Reviewers and analysts, and which model each runs on | [agents.md](references/agents.md) |
| Loop | Session start and end, definition of done, checkpoints | [loop.md](references/loop.md) |
| Version control | git, `.gitignore`, LFS, an optional GitHub remote | [version-control.md](references/version-control.md) |

Read a reference only when you reach its part. Templates for generated files are
in `assets/` (paths are relative to this skill's folder):

| Asset | Becomes |
|---|---|
| `CLAUDE.md` | `CLAUDE.md` |
| `docs/` (`README.md`, `INDEX.md`, `decisions.md`, `questions.md`, `handoff.md`, `session-report.md`) | the chosen memory modules |
| `skills/grill/`, `skills/docs-audit/`, `skills/session/` | `.claude/skills/<name>/` |
| `agents/red-team.md` | `.claude/agents/red-team.md` |
| `tools/docs_audit.py` | `tools/docs_audit.py` (+ `tools/docs_audit.json` when the defaults don't fit) |
| `hooks/block_destructive.py`, `hooks/test_block_destructive.py` | `.claude/hooks/` |
| `settings.json` | `.claude/settings.json` (keep only the parts chosen) |
| `gitignore` | `.gitignore` |

Every template has `<placeholders>` and a comment saying what to tailor. None
is copied as it is: replace every placeholder, delete what doesn't apply, and
remove the template comment.

---

## Step 0 · Look before asking

1. Confirm the session's working directory is the new project's folder. If it
   isn't, ask which folder, and move there before writing anything.
2. List the folder. Read any README, notes, brief, or reference material the
   owner put there. Anything you can learn from the files, don't ask.
3. If a `CLAUDE.md` or `docs/` already exists, this is a **retrofit**: read
   them, say what is already there, and plan to extend rather than replace.
   Never overwrite an existing file without showing the owner what changes.
4. Check whether it is already a git repository, and whether it has a remote.

## Step 1 · Purpose grill

Run the interview in [grill.md](references/grill.md). In short:

- **One question at a time.** Each comes with the options, your
  recommendation, and one line on what changes depending on the answer. Use the
  question tool when the options are discrete.
- **Most decisive first**: purpose → done-when → lifespan → who does the work
  (autonomy) → the rest.
- **Skip what the files or earlier answers already settle**, and say you did.
- **Stop when the next answer would not change the structure.** A one-off tool
  needs four or five questions, a long product ten to fifteen.

The output is a **project profile**: a short list of the answers, kept for
step 4.

## Step 2 · Choose the parts

Map the profile onto the parts using the tables in each reference. Start from
the closest **archetype** in [grill.md](references/grill.md#archetypes), then
add or drop modules by the specific answers.

**Start small.** Generate what the project needs in its first month. Everything
else becomes a **growth trigger**: a written rule saying when to add it ("split
`architecture.md` when it passes ~400 lines", "add `adr/` at the first one-way
decision"). A structure that is bigger than the work gets abandoned.

## Step 3 · Show the plan, then wait

Before writing a file, show the owner:

1. The profile, in five to ten lines.
2. The file tree you will create, with one line per file.
3. For each part, what you are adding and why, in one line, citing the answer
   that drove it. Parts you are leaving out, and the trigger that would add them.
4. What version control will do: git init, the `.gitignore` highlights, and
   whether a GitHub repository is proposed. **Creating a remote repository or
   pushing is outward-facing: it needs its own explicit yes**, separate from the
   yes to the plan.

Ask once: proceed, or change something. Apply changes and show only what
changed.

## Step 4 · Generate

Work through the parts in this order, each per its reference:

1. **Version control first** (`git init`, `.gitignore`), so secrets and private
   data are ignored before any of them exist.
2. **Memory**: the `docs/` structure, with real content from the grill, not
   empty templates. `context/` gets the purpose, scope and non-goals as
   answered. A file with nothing true to say yet is not created; its trigger is
   written down instead.
3. **Limits**: hard rules into `CLAUDE.md`; deny rules and hooks into
   `.claude/settings.json`; hook scripts and their tests.
4. **Tools**: `.mcp.json`, `tools/` scripts, the permission allowlist.
5. **Sub-agents and project skills**: copied from `assets/`, then tailored, so
   every path they name exists in this project.
6. **Instructions**: `CLAUDE.md` last, because it points at everything above.
   Keep it under ~100 lines.
7. **Record the setup**: the first decision (`D-001` or `ADR-0001`), "Project
   structure", with the profile answers that drove it and a **Revisit if**. Then
   the first session report or handoff entry.

Use absolute dates (YYYY-MM-DD) everywhere. Write docs for a human reader as
well as an agent: `docs/` is tool-neutral, and `CLAUDE.md` is the only file
written only for Claude.

## Step 5 · Verify

- Run the docs audit if one was generated (`python tools/docs_audit.py`) and fix
  every FAIL.
- Run the hook tests if a hook was generated.
- Validate `.claude/settings.json` and `.mcp.json` as JSON.
- Check every path named in `CLAUDE.md` exists.
- `git status`: nothing private is staged or unignored.
- Commit only if the owner said to (one commit, "Set up project context").
  Push only if they said yes to the remote in step 3.

## Step 6 · Hand over

Tell the owner, in a few lines:

- what was created, by part
- what was left out, and the triggers that would add it
- how to start the next session (the start routine in `CLAUDE.md`)
- open questions the grill raised that the owner still has to answer

---

## Rules

- **The purpose drives the structure.** Every generated file traces back to a
  profile answer. If you can't say which answer a file serves, don't create it.
- **Ask, don't assume, on anything outward-facing or hard to reverse**: creating
  a GitHub repository, making anything public, pushing, adding a hook that
  blocks commands.
- **Concrete content over placeholders.** A template with `TODO` in every
  section teaches the next session nothing. Fill it from the grill or leave the
  file out.
- **Don't copy a project's personality into another.** The assets are starting
  points; the lenses, hard rules and file names must be rewritten for this
  project.
- **The owner decides.** Recommend firmly, but every structural choice is theirs.
