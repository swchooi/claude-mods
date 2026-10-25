# Sub-agents and models

Sub-agents run in their own context with their own instructions and tools.
Add one when the work needs **independence** (a reviewer that hasn't seen the
author's reasoning) or **isolation** (a big read whose details shouldn't fill
the main context). Not for splitting ordinary work.

## Which ones

| Agent | Add when | Tools | Template |
|---|---|---|---|
| `red-team` | One-way decisions ahead; the `grill` skill is installed | Read, Grep, Glob (read-only) | `assets/agents/red-team.md` |
| `<source>-analyst` | A source of truth is large or awkward to read (a workbook, logs, a codebase you don't own); questions about it recur | Read-only, plus the dumper tools | Write it per project: what the source is, the tools to read it, "report counts, cite rows", never modify |

Tailoring `red-team`:

- One sentence on what the project is, so it attacks the right things.
- **What to read**: the proposal, the purpose/vision doc, the decisions it must
  respect, the doc describing the source of truth, and the grill's
  `lenses.md`.
- **What not to read**: session reports, handoffs, reviews (the author's
  reasoning). Independence is the only thing it adds.
- Any hard limits it must keep (never open a live data file).

The `grill` skill passes it only the proposal path and what is being decided.

## Models

- The main session uses the owner's chosen model; don't set it in project files.
- Set `model:` in a sub-agent's frontmatter only for a clear reason: a cheaper
  model for summarising or bulk reading, the strongest model for the red team.
- On a limited plan, say in `CLAUDE.md` which agents are expensive and when they
  may run.

## When the project builds an agent

Different layer: the product itself contains an agent (a chat sidebar that
calls tools, an automated research run). Add a design note
(`docs/design/<agent>.md`) covering what the agent may and may not do, and put
these in the definition of done for that feature:

- **Access**: read-only where possible; only data the signed-in user may see;
  named tools over free-form queries.
- **Known-answer tests**: a set of questions with known answers, rerun whenever
  the model or prompt changes. Plausible wrong answers are the typical failure.
- **Show the working**: which query or source each figure came from.
- **Trace every step**: log each model call and tool call.
- **Caps**: maximum steps and cost per request, and when it hands over to a
  human.
