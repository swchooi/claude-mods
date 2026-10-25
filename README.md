# claude-mods

My collection of Claude-related things: plugins, skills, MCP setups, mods and projects.

| path | what it is |
|---|---|
| [plugins/session-meter](plugins/session-meter) | Claude Code plugin: a coloured band above the prompt showing context tokens, room left before auto-compact, 5-hour and 7-day usage limits with reset times, and session cost in MYR (estimated from a daily USD→MYR rate) |
| [plugins/project-setup](plugins/project-setup) | Claude Code skill for starting a project: interviews you about its purpose, then sets up the parts its agent needs (CLAUDE.md, docs context structure, skills, sub-agents, limits and hooks, session loop, git and GitHub), sized to the project |
| [animation](animation) | Hand-painted cartoon kit for Claude Code (from [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)), with the short "The Last Leaf" |

## session-meter

The repo is also a Claude Code plugin marketplace (`chooi-mods`).

### Install

```bash
claude plugin marketplace add swchooi/claude-mods
claude plugin install session-meter@chooi-mods
```

Start a new session, in the terminal or the desktop app's Code tab, and the band appears after the first reply.

### Update / remove

```bash
claude plugin marketplace update chooi-mods
claude plugin update session-meter@chooi-mods
claude plugin uninstall session-meter@chooi-mods
```

## Skills

### project-setup

Sets up a new project so Claude Code works well in it. It starts with a **purpose grill**: one question at a time (what it's for, what done looks like, how long it lives, who does the work, what is read-only or sensitive, what would be expensive to undo), each with options and a recommendation. Then it shows a plan and, once you agree, generates only the parts the project needs:

| Part | What it sets up |
|---|---|
| Memory | `docs/` context structure: from a single `CLAUDE.md` for a one-off up to context, decisions, questions, roadmap, sessions or handoff, with growth triggers for the rest |
| Instructions | `CLAUDE.md` (under ~100 lines), path rules, project skills (`grill`, `docs-audit`, `session`) |
| Tools | MCP servers, `tools/` scripts, the permission allowlist |
| Limits | Hard rules, deny rules, the `block_destructive` guardrail hook, when to ask you, budget |
| Sub-agents | `red-team` reviewer, source analysts, model choice |
| Loop | Start and end of a session, definition of done, milestone checkpoints |
| Version control | `git init` and `.gitignore` first; a GitHub repository only after you say yes |

Install:

```bash
claude plugin install project-setup@chooi-mods
```

Then, in a new project's folder, ask Claude to "set up this project" (or run `/project-setup`).

## animation

Open `animation/` in Claude Code and ask for a video, for example: "Read ANIMATION_GUIDE.md, then make a 15-second video of Clawd …".
It needs Node.js, Chrome or Edge, and ffmpeg. To render the current film:

```bash
npm install
node render.mjs --frames --workers=4
node render.mjs --encode --out=out/video.mp4
```
