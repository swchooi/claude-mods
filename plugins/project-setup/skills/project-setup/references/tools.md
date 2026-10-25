# Tools: MCP, scripts, permissions

Tools let the agent read data and change things. Give it the tools the work
needs, prefer narrow ones to broad ones, and make read-only the default where
the source is precious.

## Choosing tools

| Need from the grill | Tool | Example |
|---|---|---|
| Drive a desktop app or service | MCP server in `.mcp.json` | Revit MCP; Playwright MCP for UI checks |
| Read a file format the agent can't read well | A dumper in `tools/` (read-only, prints text) | `tools/xlsx/dump_sheet.py` for a workbook |
| Inspect a live system | A read-only wrapper script, listed first in `CLAUDE.md` | `bin/srv ps|disk|health` over SSH |
| Keep a local copy of remote config | A one-way mirror script, never edited by hand | `tools/Sync-ServerContext.ps1` |
| Repeatable checks on the docs | `tools/docs_audit.py` (from `assets/tools/`) | |
| Verify a UI change | Browser tool or Playwright, named in the definition of done | |

**Prefer named, narrow tools over free-form ones.** A `dump_sheet` tool is safer
than letting the agent open the workbook with a library that can write; a
`query_metric` tool is safer than raw SQL.

**Read-only by construction** when the source must not change: the tool itself
refuses writes (phonediff's `adb()` allowlist), rather than relying on a rule
in `CLAUDE.md`.

## .mcp.json

Project-scoped servers go in `.mcp.json` at the root, committed if they hold no
secrets. Secrets come from environment variables, never inline. Name the server
and what it is for in `CLAUDE.md`. Ask the owner before adding a server that
can write to an external system.

## tools/

One folder per tool, each with a `README.md` (what it does, how to run it,
what it never does). Config and code only; outputs go to `artifacts/` or a
git-ignored folder.

## Permission allowlist

`.claude/settings.json` → `permissions.allow`. Add the read-only commands the
project runs often so sessions aren't interrupted, and nothing that writes
outside the project or touches a remote:

```json
"allow": [
  "Bash(git status:*)",
  "Bash(git diff:*)",
  "Bash(git log:*)",
  "Bash(python tools/docs_audit.py:*)"
]
```

Add the project's test and lint commands once they exist. Deny rules belong to
[limits.md](limits.md).
