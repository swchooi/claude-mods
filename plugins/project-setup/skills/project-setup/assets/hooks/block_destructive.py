#!/usr/bin/env python3
"""PreToolUse hook: block destructive or secret-touching shell commands (Bash and PowerShell tools).

Permission deny rules only match a command's prefix, so `git push origin main --force`
slips past `Bash(git push --force:*)`, and Read-tool denies don't stop `cat .env`.
This hook inspects the whole command text.

It matches text, not parsed shell, so a command that merely *mentions* a blocked pattern
(e.g. inside an echo or a commit message) is blocked too. That fails safe; put such text
in a file instead (e.g. `git commit -F msgfile`).

Reads the hook JSON on stdin; exits 2 (block, reason on stderr) or 0 (allow).
Malformed input exits 0. The settings.json wrapper turns any *other* failure (missing
interpreter, crash) into a block.
"""
from __future__ import annotations

import json
import os
import posixpath
import re
import sys

SEG = r"[^;&|\n]*"  # rest of the current shell segment

# Recursive deletes are allowed only under these (build output, caches, scratchpads).
# Edit for the project: add its own build and cache folders (e.g. \.godot, target, .next).
SAFE_RELATIVE = re.compile(r"^(build|builds|dist|out|export|\.cache|node_modules)(/|$)", re.IGNORECASE)
SAFE_ABSOLUTE = re.compile(r"^(/[a-z]|[a-z]:)/temp/claude/", re.IGNORECASE)


def git(sub: str) -> re.Pattern:
    return re.compile(rf"\bgit\b{SEG}?\b{sub}\b({SEG})")


GIT_RULES: list[tuple[re.Pattern, re.Pattern | None, str]] = [
    (git("push"), re.compile(r"(^|\s)(--force\S*|-[a-zA-Z]*f[a-zA-Z]*|--delete|-d|\+\S+|:\S+)(?=\s|$)"),
     "force-push or remote branch deletion"),
    (git("reset"), re.compile(r"(^|\s)--hard\b"), "git reset --hard discards uncommitted work"),
    (git("clean"), re.compile(r"(^|\s)(-[a-zA-Z]*f[a-zA-Z]*|--force)(?=\s|$)"), "git clean -f deletes untracked files"),
    (git("branch"), re.compile(r"(^|\s)(-[a-zA-Z]*D[a-zA-Z]*)(?=\s|$)|--delete\b.*--force|--force\b.*--delete"),
     "force-deleting a branch"),
    (git("stash"), re.compile(r"^\s*(drop|clear)\b"), "dropping stashed work"),
    (git("checkout"), re.compile(r"(^|\s)(-f|--force)(?=\s|$)"), "git checkout -f discards uncommitted work"),
    (git("switch"), re.compile(r"(^|\s)(-f|--force|--discard-changes)(?=\s|$)"), "git switch discarding uncommitted work"),
    (git("worktree"), re.compile(r"^\s*remove\b.*(\s(-f|--force))(?=\s|$)"), "force-removing a worktree"),
    (git("update-ref"), re.compile(r"(^|\s)-d(?=\s|$)"), "deleting a ref"),
    (git("gc"), re.compile(r"--prune=(now|all)\b"), "pruning unreachable objects"),
    (git("reflog"), re.compile(r"^\s*(expire|delete)\b"), "rewriting the reflog"),
    (re.compile(rf"\bgit\b{SEG}?\bfilter-(branch|repo)\b()"), None, "history rewrite"),
]

# `git restore <paths>` / `git checkout [<ref>] -- <paths>` discard working-tree changes.
DISCARD_RE = re.compile(rf"\bgit\b{SEG}?\b(restore|checkout)\b({SEG})")

DELETE_CMD = re.compile(
    rf"(?:^|[\s;&|(\"'])(rm|Remove-Item|ri|rmdir|rd|del|erase)(?=\s)({SEG})",
    re.IGNORECASE,
)
# rm-style short-flag clusters (-r, -rf, -Rfv) or PowerShell -Recurse (any prefix, optional :$true), or cmd /s.
RECURSIVE_FLAG = re.compile(r"^(-[fivdIR]*[rR][fivdIR]*|--recursive|-rec\w*(:\$?true)?|/s)$", re.IGNORECASE)
WIN_SWITCH = re.compile(r"^/[a-zA-Z]$")  # cmd.exe switches like /s /q
PIPE_DELETE = re.compile(
    r"\b(Get-ChildItem|gci|ls|dir)\b[^;\n|]*\s-r\w*[^;\n|]*\|\s*(Remove-Item|ri|rm|del|erase)\b",
    re.IGNORECASE,
)

SECRET_RE = re.compile(r"(?<![\w.$-])\.env(\.[\w.-]+)?(?![\w-])|(?<![\w.-])secrets[/\\]")


def norm_target(raw: str) -> str | None:
    """Normalised forward-slash path, or None if it tries to climb with '..'."""
    t = raw.strip("\"'").replace("\\", "/")
    if any(part == ".." for part in t.split("/")):
        return None
    t = posixpath.normpath(t)
    return t[2:] if t.startswith("./") else t


def is_safe_target(raw: str) -> bool:
    t = norm_target(raw)
    if t is None or t in ("", "."):
        return False
    return bool(SAFE_RELATIVE.match(t) or SAFE_ABSOLUTE.match(t))


def check_git(cmd: str) -> str | None:
    for pattern, flags, reason in GIT_RULES:
        for m in pattern.finditer(cmd):
            if flags is None or flags.search(m.group(1)):
                return reason
    return None


def check_discard(cmd: str, cwd: str) -> str | None:
    for m in DISCARD_RE.finditer(cmd):
        sub, rest = m.group(1), m.group(2)
        tokens = rest.split()
        if sub == "restore":
            if "--staged" in tokens and "--worktree" not in tokens and "-W" not in tokens:
                continue  # only unstages
            paths = [t for t in tokens if not t.startswith("-")]
        else:
            if "--" not in tokens:
                paths = [t for t in tokens if t in (".", ":/")]
            else:
                paths = tokens[tokens.index("--") + 1:]
        for p in paths:
            t = p.strip("\"'")
            if t in (".", ":/") or t.endswith(("/", "\\")) or any(c in t for c in "*?[") \
                    or os.path.isdir(os.path.join(cwd, t)):
                return f"git {sub} on a directory or pattern discards uncommitted work"
    return None


def check_delete(cmd: str) -> str | None:
    if PIPE_DELETE.search(cmd):
        return "recursive listing piped into a delete"
    for m in DELETE_CMD.finditer(cmd):
        tokens = m.group(2).split()
        if not any(RECURSIVE_FLAG.match(t) for t in tokens):
            continue
        targets = [t for t in tokens if not t.startswith("-") and not WIN_SWITCH.match(t)]
        if not targets or not all(is_safe_target(t) for t in targets):
            return f"recursive delete ({m.group(1)}) outside build/cache/scratchpad directories"
    return None


def check_secrets(cmd: str) -> str | None:
    if SECRET_RE.search(cmd):
        return "command touches .env or secrets/ files (secrets are off-limits to agents)"
    return None


def reason_to_block(cmd: str, cwd: str = ".") -> str | None:
    return check_git(cmd) or check_discard(cmd, cwd) or check_delete(cmd) or check_secrets(cmd)


def main() -> int:
    try:
        data = json.load(sys.stdin)
        cmd = data.get("tool_input", {}).get("command", "")
        cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or "."
    except (ValueError, AttributeError):
        return 0
    if not isinstance(cmd, str) or not cmd:
        return 0
    reason = reason_to_block(cmd, cwd)
    if reason:
        print(
            f"Blocked by .claude/hooks/block_destructive.py: {reason}.\n"
            "If this is genuinely needed, stop and ask the owner to run it themselves.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
