# claude-mods

My collection of Claude-related things: plugins, skills, MCP setups, mods and projects.

| path | what it is |
|---|---|
| [plugins/session-meter](plugins/session-meter) | Claude Code plugin: a coloured band above the prompt showing context tokens, room left before auto-compact, 5-hour and 7-day usage limits with reset times, and session cost in MYR (estimated from a daily USD→MYR rate) |
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

## animation

Open `animation/` in Claude Code and ask for a video, for example: "Read ANIMATION_GUIDE.md, then make a 15-second video of Clawd …".
It needs Node.js, Chrome or Edge, and ffmpeg. To render the current film:

```bash
npm install
node render.mjs --frames --workers=4
node render.mjs --encode --out=out/video.mp4
```
