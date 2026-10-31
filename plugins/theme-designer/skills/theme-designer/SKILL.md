---
name: "theme-designer"
description: "Design a custom app or website theme by interviewing the user, showing visual options, then packaging chosen colors, containers, motion, type, icons and density as a CSS theme package."
---

# Theme designer

Build a custom UI theme with the user in stages: grill them with quick multiple-choice questions, show 3 visual options, let them pick, then write the choice into a CSS variables file. Repeat per layer. Finish by packaging it so they can reuse it in any project.

The user is a beginner at theming. Keep each explanation brief, and when restating a term from an earlier stage, define it again in a few words (e.g. "tokens, the named values like --accent").

## Ground rules

- One layer at a time. Never ask about everything up front.
- Grill before showing: use AskUserQuestion (max 4 questions, 2-4 options each, "Show me options" is a valid option). If the user is unattended, take sensible defaults and say which.
- Show options visually (inline widget, or a Design artifact if available), never as a list of hex codes. Each option previews the same small mock UI so they compare like with like. Include a light/dark toggle in every preview.
- Mark one option "Recommended" based on their answers, and say why in one or two short bullets after the widget.
- Put a "Use this" / "Use my picks" button on the widget that sends the choice back as a prompt.
- After each pick, update ONE theme CSS file (not a new file per layer) and send it with SendUserFile. Explain usage in short bullets plus one HTML example.
- Mixed answers are fine: map options to use cases (e.g. flat containers for table rows, elevated for cards and dialogs).

## Stage 0 — Primer (2-3 short paragraphs max)

A theme = reusable design decisions (tokens) for: colors, typography, shape/containers, motion, icons, density. Where it lives decides how it's built: web apps use CSS variables; VS Code uses a JSON color map; Samsung phones use Theme Park (Good Lock); Windows uses accent + wallpaper + mode. Beginner rules: one accent plus neutrals, text contrast at least 4.5:1, define light and dark.

## Stage 1 — Colors

Ask: platform (phone theme, code editor, app/site they're building, desktop), vibe (multi-select: calm and minimal, bold and vibrant, dark and moody, retro/playful), mode (light, dark, both), color family (cool, warm, earthy, monochrome).

If the platform isn't a web app, adapt the deliverable (VS Code: color theme JSON + package.json for a local extension; Samsung: Theme Park step-by-step with the palette hexes). The rest of this skill assumes a web app.

Show 3 palettes. Each defines the same roles in light AND dark:
`--bg` (page), `--surface` (cards/panels/inputs), `--surface-hover`, `--border`, `--text`, `--text-muted`, `--accent`, `--accent-hover`, `--accent-soft` (tinted bg), `--on-accent` (text on accent), `--success`, `--danger`.

Dark-mode rules: tinted near-black backgrounds (never pure #000), a lighter accent than in light mode, dark text on accent buttons.

File structure for light/dark:
```css
:root { /* light + all non-color tokens */ color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { /* dark colors */ color-scheme: dark; } }
:root[data-theme="dark"] { /* same dark colors */ color-scheme: dark; }
```

## Stage 2 — Containers and motion

Explain: containers = radius, edge (border / shadow / tint), elevation, spacing. Motion = duration, easing, what moves, reduced-motion support.

Show 3 container styles in their palette:
- A Flat outlined: 8px radius, 1px border, no shadow — rows, tables, stat tiles
- B Soft elevated: 12px radius, soft shadow — cards, menus, dialogs (shadow grows with height)
- C Tinted panel: 16px radius, accent-soft fill — callouts, empty states, featured

Show 3 motion styles with a Replay button and press effect:
- Snappy 120ms ease-out — hover, press, menus
- Smooth 280ms cubic-bezier(.2,.8,.2,1) — content entering, dialogs
- Springy 450ms cubic-bezier(.34,1.56,.64,1) — rare delight only

Tokens: `--radius`, `--radius-lg`, `--radius-xl`, `--radius-pill`, `--space-1..7`, `--shadow-1..3`, `--overlay`, `--dur-fast/base/slow`, `--ease-out`, `--ease-spring`. Dark mode gets stronger shadows plus a 1px `--card-edge`, because shadows barely show on dark backgrounds.

Classes: `.row`, `.tile`, `.card` (+ `.is-clickable`), `.menu`, `.menu-item`, `.backdrop`, `.dialog`, `.panel`, `.animate-enter`, `.animate-pop`, `.stagger` (children get `style="--i:N"`). Always include:
```css
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 1ms !important; animation-delay: 0ms !important; transition-duration: 1ms !important; } }
```

## Stage 3 — Big-impact items: typography, icons, layout and density

Ask: app type (dashboard/data-heavy, workflow/forms, content/reading, mix), device (desktop, phone, both), font feel (neutral, friendly, technical, editorial), icon feel (thin, regular, rounded, show me options).

Show, in one widget with selectable cards and a "Use my picks" button:
- 3 font pairings from Google Fonts matching the feel, each previewing a heading, body line, a KPI number with tabular figures, and a mono ID. Technical examples: IBM Plex Sans + Mono, Geist + Geist Mono, Space Grotesk + Inter + JetBrains Mono.
- 3 icon sets: Lucide (adjustable stroke), Tabler (2px, 5,800+ icons), Phosphor (6 weights). Same 6 icons in each.
- 3 density options: comfortable everywhere, compact everywhere, adaptive.

Tokens: `--font-sans`, `--font-mono`, `--fs-xs..2xl`, `--fs-kpi` (fs = font size), `--fw-*` (font weight), `--lh-*` (line height), `--ls-*` (letter spacing), `--icon-sm/md/lg`, `--page-max`, `--content-max`, `--sidebar-w`, `--topbar-h`, `--gutter`, `--control-h`, `--tap-min`, `--row-pad-*`, `--cell-pad-*`, `--fs-table`.

Adaptive density pattern:
```css
@media (pointer: coarse) { :root { --control-h: 44px; } }
@media (min-width: 1024px) and (pointer: fine) {
  .table, [data-density="compact"] { /* compact values */ }
  [data-density="comfortable"] { /* comfortable values, must come after */ }
}
```
Breakpoints can't use CSS variables, so document them in a header comment: phone < 640px, tablet 640-1023px, desktop >= 1024px.

Also add: base styles (body, h1-h4, `.label`, `.caption`, `.prose`, `.mono`, `.num`, `.kpi`), layout (`.container`, `.stack`, `.cluster`, `.grid`, `.app-shell` with `.topbar`/`.sidebar`/`.main`), tables (`.table-wrap`, `.table`, sticky header, `.num` right-aligned), controls (`.btn`, `.btn-primary`, `.btn-icon`, inputs at 16px font to stop iPhone zoom, `.badge`), icon classes.

Put a header comment at the top of the CSS with the font/icon `<link>` tags, a section index, and "which container / which motion / density" usage maps.

## Stage 4 — Offer the remaining layers (optional)

Components: form controls (checkbox, toggle, radio, validation), navigation (tabs, breadcrumbs, mobile bottom bar), data display (chart palette, avatars), feedback (toasts, banners, skeletons, spinners, empty states). Finishing touches: states, focus rings, scrollbars, selection color, brand assets, UI copy voice. Same grill → options → write loop.

## Stage 5 — Package for reuse

Create a folder named after the theme (kebab-case) containing:
- `<theme>.css` — the theme file
- `all.css` — `@import` of fonts, icons, then `./<theme>.css` (one-link entry)
- `theme.js` — light/dark helper exposing `get()`, `set('light'|'dark'|'system')`, `toggle()`, `isDark()`; saves to localStorage; applies on load (tell users to load it in `<head>` to avoid a flash); any `[data-theme-toggle]` element toggles on click; wrap storage access in try/catch
- `package.json` — name, version 1.0.0, `style: all.css`, `exports` for `.`, `./all.css`, `./theme.css`, `./theme.js`, `files` list, `sideEffects` for css and js
- `demo.html` — every component on one page (app shell, KPI tiles, table, rows, cards with a form, panel, menu, dialog, pop badge, prose, theme toggle)
- `README.md` — three ways to use it (copy into static folder incl. Flask `url_for`; `npm install <path>` or `github:user/repo` then `import '<theme>'`; jsDelivr `cdn.jsdelivr.net/gh/user/repo@1.0.0/all.css` for public repos with a pinned version), parallel `<link>` tags for faster loading, light/dark API, class cheat sheet, token prefix glossary, and how to override tokens per project without editing the package

Verify before delivering: package.json parses, theme.js parses, zip lists all files, render demo.html headless in light, dark and phone widths if Playwright is available (CDN fonts/icons may be blocked in the sandbox; that's expected), and check compact table padding on desktop vs comfortable on phone. Zip the folder and send it.

## Wrap-up message

One line on what came out, the file, and the single most useful next step (usually: push to GitHub and tag v1.0.0 so every project can load it by URL). No recap of steps.