# Version control: git, .gitignore, GitHub

Set up first, before any other file exists, so private data and secrets are
ignored from the start. Local git is cheap and reversible; a remote is
outward-facing and needs the owner's explicit yes.

## Choose the level

From grill question 12, checked against the sensitive-data answer:

| Level | When | Examples |
|---|---|---|
| **None** | Truly throwaway (hours), or the folder only holds outputs | a scratch analysis |
| **Local git** | Default. History and undo without anything leaving the machine. Required when data is private and there is no strong reason for a remote | spendingrecords (financial data), general |
| **Private GitHub** | Backup off the machine, CI, an agent that opens PRs, work from another machine or a cloud session | investiapp, driving-game |
| **Public GitHub** | The owner wants to share it. Ask twice: everything committed so far becomes public, including history | claude-mods |
| **Repo lives elsewhere** | The source of truth is a repo on a server; the local folder holds a read-only mirror and is not itself a repo | kittyserver |

Recommend **local git** unless an answer calls for a remote. Private data
pushes the recommendation toward local; an unattended agent that opens PRs
pushes it toward private GitHub.

## Local setup

Run in this order:

1. `git init -b main`
2. Write `.gitignore` **before** the first `git add`. Start from
   `assets/gitignore` and add the project's own entries:
   - live or private data (the workbook, device listings, exports), by path
   - `.env` and `.env.*` except `.env.example`, `secrets/`
   - `.claude/settings.local.json`, `.claude/worktrees/`
   - build output, caches, `node_modules/`, intermediates that quote prompts
     (`artifacts/*/work/`)
3. `.gitattributes`: `* text=auto` (Windows line endings), and LFS patterns if
   binaries will be committed (below).
4. Check nothing private is about to be committed:
   `git status --short --ignored` and read the list.
5. First commit only if the owner agreed to it in the plan:
   "Set up project context", one commit.

**Synced folders.** A repository inside OneDrive, Dropbox or similar works,
but the sync client can conflict on files in `.git/`. Note it in `CLAUDE.md`
if the project lives in one, and prefer a non-synced path for repositories
with heavy git activity.

## Large binaries

If the project will commit images, audio, video, models or design files over a
few MB:

- With a GitHub remote: Git LFS (`git lfs install`, `git lfs track "*.png"`
  etc. into `.gitattributes`) before the first such file is added. LFS has
  storage and bandwidth quotas on GitHub; mention them to the owner.
- Local only: plain git is fine; LFS adds nothing without a remote.
- Outputs that can be rebuilt from inputs: commit the inputs, ignore the outputs
  unless the owner wants them versioned.

## GitHub (only on an explicit yes)

Creating a repository and pushing publish the code to an external service. Ask
for it separately from the plan, naming the owner/name and visibility.

1. `gh auth status`. If not signed in, ask the owner to run `gh auth login`
   themselves; never handle their credentials.
2. Re-check for private data: `git ls-files` and read the list. Search for
   likely secrets (`.env`, `key`, `token`, `password` in committed files).
3. `gh repo create <owner>/<name> --private --source . --remote origin`
   (`--public` only if the owner chose public).
4. `git push -u origin main`, only if the owner said to push.
5. Record the remote in `CLAUDE.md` and as a decision (`D-00N`: why this
   visibility, what must never be pushed).

For an agent that works unattended through PRs, also decide with the owner:
which branch deploys (e.g. `production`), whether CI runs on PRs, and the hard
rule that the agent never pushes or merges to the deploying branch unless told
in that session.

## Rules for CLAUDE.md

Write the project's version-control conventions into `CLAUDE.md` →
Conventions. Defaults from the owner's projects:

- Commit only when the owner asks; one commit per logical change; the message
  says what changed and why.
- Never add a remote, push, or change visibility without asking.
- Never commit live data or secrets; the `.gitignore` entries and why.
- No force-push, `reset --hard` or history rewrites (the guardrail hook, if
  installed, enforces this).
