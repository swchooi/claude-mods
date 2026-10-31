#!/usr/bin/env python3
"""Repo checks: JSON files parse, marketplace.json matches each plugin.json, plugin tests pass.

Run: python scripts/check_repo.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules"}


def check_json() -> list[str]:
    errors = []
    for p in ROOT.rglob("*.json"):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append(f"{p.relative_to(ROOT)}: invalid JSON ({e})")
    return errors


def check_marketplace() -> list[str]:
    errors = []
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    listed = set()
    for entry in market["plugins"]:
        name = entry["name"]
        listed.add(name)
        manifest = ROOT / entry["source"] / ".claude-plugin" / "plugin.json"
        if not manifest.exists():
            errors.append(f"{name}: {manifest.relative_to(ROOT)} not found")
            continue
        plugin = json.loads(manifest.read_text(encoding="utf-8"))
        for key in ("name", "version", "description"):
            if entry.get(key) != plugin.get(key):
                errors.append(f"{name}: '{key}' differs between marketplace.json and plugin.json")
    for d in (ROOT / "plugins").iterdir():
        if d.is_dir() and d.name not in listed:
            errors.append(f"plugins/{d.name} is not listed in marketplace.json")
    return errors


def run_tests() -> list[str]:
    errors = []
    for test in sorted(ROOT.glob("plugins/*/skills/*/assets/hooks/test_*.py")):
        r = subprocess.run([sys.executable, str(test)], capture_output=True, text=True)
        if r.returncode != 0:
            errors.append(f"{test.relative_to(ROOT)} failed:\n{r.stdout}{r.stderr}")
    return errors


def main() -> int:
    errors = check_json() + check_marketplace() + run_tests()
    for e in errors:
        print(f"FAIL {e}")
    print("all checks passed" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
