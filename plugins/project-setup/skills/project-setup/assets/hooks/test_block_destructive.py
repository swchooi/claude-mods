#!/usr/bin/env python3
"""Tests for block_destructive.py, including the exact wiring in .claude/settings.json.

Run: python .claude/hooks/test_block_destructive.py
(Also runs from the project-setup skill's assets/hooks/, against the settings.json template.)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).with_name("block_destructive.py")
REPO = HOOK.parent.parent.parent
# Inside the project-setup skill (not a generated project), assets/ stands in for the project root.
TEMPLATE = not (REPO / ".claude" / "settings.json").exists()
if TEMPLATE:
    REPO = HOOK.parent.parent

BLOCK = [
    # force-push / remote deletion
    "git push --force",
    "git push -f",
    "git push origin main --force",
    "git push origin main -f",
    "git push --force-with-lease origin main",
    "git -C /d/dev/driving-game push origin +main",
    "git push origin --delete feature/x",
    "git push origin :feature/x",
    "git status && git push -f origin main",
    # discarding work / history
    "git reset --hard",
    "git reset --hard HEAD~3",
    "git clean -fdx",
    "git clean -f",
    "git branch -D feature/x",
    "git branch --delete --force feature/x",
    "git stash drop",
    "git stash clear",
    "git checkout -- .",
    "git checkout .",
    "git checkout -f main",
    "git checkout HEAD -- docs/",
    # find that deletes
    "find . -delete",
    "find . -name '*.tmp' -delete",
    "find src -name x -exec rm {} +",
    "find . -type f -execdir rm -f {} \\;",
    "find -name x -delete",
    "find build ../src -delete",
    "ls | xargs -I{} rm -rf {}",
    "git checkout -- docs",
    "git switch -f main",
    "git switch --discard-changes main",
    "git restore .",
    "git restore docs/",
    "git restore docs",
    "git restore '*.md'",
    "git restore --staged --worktree docs/README.md docs",
    "git worktree remove --force ../wt",
    "git worktree remove -f ../wt",
    "git update-ref -d refs/heads/main",
    "git gc --prune=now",
    "git filter-branch --tree-filter 'x' HEAD",
    "git filter-repo --path secrets",
    "git reflog expire --expire=now --all",
    "git reflog delete HEAD@{1}",
    # recursive deletes
    "rm -rf docs",
    "rm -rf /",
    "rm -fr .",
    "rm -r -f src",
    "rm -Rfv src",
    "rm --recursive --force assets",
    "rm -rf build docs",
    "rm -rf $DIR",
    "rm -rf build/../docs",
    "rm -rf ./build/../../driving-game",
    "rm -rf X/temp/claude/../../docs",
    "rm -rf relative/temp/claude/x",
    "cd x && rm -rf ../driving-game",
    "Remove-Item -Recurse -Force docs",
    "Remove-Item docs -Recurse",
    "Remove-Item docs -Recurse:$true",
    "Remove-Item -Path docs -Recurse -Force",
    "Get-ChildItem docs -Recurse | Remove-Item -Force",
    "gci -r docs | rm",
    "rm -r -fo docs",
    "rd /s /q docs",
    "rmdir /S docs",
    'powershell -Command "Remove-Item -Recurse -Force docs"',
    'bash -c "rm -rf docs"',
    # secrets
    "cat .env",
    "Get-Content .env.staging",
    "type .env.local",
    "cp env.example .env",
    "grep TOKEN config/.env",
    "ls secrets/",
    "cat ./secrets/steam.txt",
]

ALLOW = [
    "git status",
    "git push",
    "git push origin main",
    "git push -u origin feature/x",
    "git push origin main:main",
    "git push https://github.com/o/r.git main",
    "git reset HEAD file.txt",
    "git reset --soft HEAD~1",
    "git clean -n",
    "git branch -d merged-branch",
    "git branch feature/x",
    "git stash",
    "git stash pop",
    "git checkout main",
    "git checkout -b feature/x",
    "git checkout -- docs/README.md",
    "git switch main",
    "git restore docs/README.md",
    "git restore --staged docs/README.md",
    "git restore --staged docs",
    "git worktree add ../wt",
    "git worktree remove ../wt",
    "git gc",
    "git rebase main",
    "git commit --amend -m msg",
    "git log --oneline -5",
    "git diff --stat",
    "rm file.txt",
    "rm -f build.log",
    "rm -rf build",
    "rm -rf ./build/windows",
    "rm -rf dist",
    "rm -rf node_modules",
    "rm -rf export/linux",
    "rm -rf /g/TEMP/claude/D--dev-project/abc/scratchpad/auditfix",
    "Remove-Item build.log",
    "Remove-Item -Force build.log",
    "Remove-Item -Recurse -Force build",
    "Remove-Item -Recurse G:\\TEMP\\claude\\proj\\scratchpad\\x",
    "Get-ChildItem docs -Recurse | Select-String Q-001",
    "find . -name '*.md'",
    "find build -name '*.o' -delete",
    "find node_modules -type d -name .cache -exec rm -rf {} +",
    "find . -name x -exec grep -l rm {} +",
    "python tools/docs_audit.py --quiet",
    "grep -rf patterns.txt docs",
    "grep -r process.env src",
    "echo $env:PATH",
    "cat env.example",
    "ls .envrc",
    "dir /s",
    "",
]


def run_hook(cmd: str) -> int:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(REPO)})
    return subprocess.run([sys.executable, str(HOOK)], input=payload, text=True,
                          capture_output=True).returncode


def wiring_tests() -> list[str]:
    """Run the exact command configured in settings.json through bash, like Claude Code does."""
    bash = shutil.which("bash")
    if not bash or "system32" in bash.lower():
        return ["SKIP wiring: no POSIX bash on PATH (WSL bash is not used for hooks)"]
    settings_path = REPO / ("settings.json" if TEMPLATE else ".claude/settings.json")
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    commands = [h["command"] for entry in settings["hooks"]["PreToolUse"]
                if "Bash" in entry["matcher"] for h in entry["hooks"]]
    if TEMPLATE:
        commands = [c.replace("$CLAUDE_PROJECT_DIR/.claude/hooks/block_destructive.py", str(HOOK))
                    for c in commands]
    if len(commands) != 1:
        return [f"wiring: expected 1 Bash PreToolUse hook, found {len(commands)}"]
    hook_cmd = commands[0]
    env_ok = {"PATH": __import__("os").environ["PATH"], "CLAUDE_PROJECT_DIR": str(REPO)}
    env_no_python = {"PATH": "", "CLAUDE_PROJECT_DIR": str(REPO)}
    cases = [
        ("blocks a force-push", "git push origin main --force", env_ok, 2),
        ("allows git status", "git status", env_ok, 0),
        ("fails closed with no interpreter", "git status", env_no_python, 2),
    ]
    failures = []
    for name, cmd, env, want in cases:
        payload = json.dumps({"tool_input": {"command": cmd}})
        rc = subprocess.run([bash, "-c", hook_cmd], input=payload, text=True,
                            capture_output=True, env=env).returncode
        if rc != want:
            failures.append(f"wiring: {name} -> exit {rc}, want {want}")
    return failures


def main() -> int:
    failures = [f"should BLOCK: {c}" for c in BLOCK if run_hook(c) != 2]
    failures += [f"should ALLOW: {c}" for c in ALLOW if run_hook(c) != 0]
    if subprocess.run([sys.executable, str(HOOK)], input="not json", text=True,
                      capture_output=True).returncode != 0:
        failures.append("malformed input should exit 0")
    wiring = wiring_tests()
    skips = [w for w in wiring if w.startswith("SKIP")]
    failures += [w for w in wiring if not w.startswith("SKIP")]
    for line in skips + [f"FAIL {f}" for f in failures]:
        print(line)
    total = len(BLOCK) + len(ALLOW) + 1 + (0 if skips else 3)
    print(f"{total - len(failures)}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
