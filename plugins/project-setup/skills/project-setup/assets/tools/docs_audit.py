#!/usr/bin/env python3
"""Docs audit: catch the drift in docs/ that is mechanically checkable.

Groups:
  STRUCTURE    a doc not listed in the index, a docs folder with no README (per-folder mode)
  LINKS        a relative link to a file or heading anchor that doesn't exist
  IDS          an ID referenced but never defined, defined twice, or a gap in numbering (WARN)
  FRONTMATTER  a doc missing a required frontmatter key (only if configured)
  STALE        a snapshot doc past its `stale_after` date (WARN: re-verify it)

Config: tools/docs_audit.json beside this script (optional; defaults below).
Exit 1 on any FAIL (2 with --hook-exit, for a Claude Code Stop hook), else 0.

Run: python tools/docs_audit.py [--quiet] [--only GROUP]... [--repo PATH] [--hook-exit]
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_CONFIG = {
    # Files to scan: globs relative to the repo root.
    "scan": ["docs/**/*.md", "*.md", ".claude/skills/**/*.md", ".claude/agents/*.md"],
    # Globs never scanned (read-only sources, archives, snapshot reviews).
    "exclude": ["reference/**", "docs/archive/**", "reviews/**", ".claude/worktrees/**", "node_modules/**"],
    # "file": every doc under docs/ must be linked from this index.
    # "per-folder": every doc must be linked from its folder's README.md.
    "index": {"mode": "file", "path": "docs/INDEX.md"},
    # ID kinds. `defined` regexes (multiline) capture the ID where it is defined;
    # everything else matching `pattern` counts as a reference.
    "ids": [
        {"name": "decision", "pattern": r"\bD-\d{3}\b", "defined": [r"^#{2,4} (D-\d{3})\b"]},
        {"name": "question", "pattern": r"\bQ-\d{3}\b", "defined": [r"^- \[[ xX]\] \*\*(Q-\d{3})\*\*"]},
        {"name": "task", "pattern": r"\bT-\d{3}\b", "defined": [r"^\|\s*(T-\d{3})\s*\|", r"^- \*\*(T-\d{3})\*\*"]},
        {"name": "milestone", "pattern": r"\bM-\d{2}\b", "defined": [r"^\|\s*(M-\d{2})\s*\|", r"^#{2,4} (M-\d{2})\b"]},
    ],
    # Required frontmatter keys for docs matching these globs. Empty = group off.
    "frontmatter": {"paths": [], "required": ["title"]},
}

FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


class Report:
    def __init__(self, quiet: bool):
        self.quiet = quiet
        self.counts = Counter()

    def add(self, level: str, group: str, where: str, msg: str) -> None:
        self.counts[level] += 1
        if level == "OK" and self.quiet:
            return
        print(f"{level:<4} {group:<11} {where}  {msg}" if where else f"{level:<4} {group:<11} {msg}")


def load_config(repo: Path) -> dict:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    path = Path(__file__).with_name("docs_audit.json")
    if path.exists():
        cfg.update(json.loads(path.read_text(encoding="utf-8")))
    return cfg


def rel(p: Path, repo: Path) -> str:
    return p.relative_to(repo).as_posix()


def matches(path: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, g) or fnmatch.fnmatch(path, g.replace("**/", "")) for g in globs)


def collect(repo: Path, cfg: dict) -> list[Path]:
    seen = {}
    for g in cfg["scan"]:
        for p in repo.glob(g):
            if p.is_file() and not matches(rel(p, repo), cfg["exclude"]):
                seen[p.resolve()] = p
    return sorted(seen.values())


def strip_code(text: str) -> str:
    """Blank out fenced blocks, inline code and HTML comments, keeping line numbers."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    return INLINE_CODE.sub(blank, FENCE.sub(blank, HTML_COMMENT.sub(blank, text)))


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip("\"'")
    return out


def slugs(text: str) -> set[str]:
    """GitHub-style heading anchors, including -1, -2 suffixes for duplicates."""
    out, count = set(), Counter()
    for h in HEADING.findall(strip_code(text)):
        h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)  # link text only
        s = re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
        out.add(s if count[s] == 0 else f"{s}-{count[s]}")
        count[s] += 1
    return out


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def check_structure(repo, cfg, files, texts, r: Report):
    mode = cfg["index"].get("mode", "file")
    docs = [p for p in files if rel(p, repo).startswith("docs/")]
    if not docs:
        r.add("OK", "STRUCTURE", "", "no docs/ folder; nothing to index")
        return
    if mode == "per-folder":
        folders = {p.parent for p in docs}
        missing = 0
        for folder in sorted(folders):
            readme = folder / "README.md"
            if not readme.exists():
                r.add("WARN", "STRUCTURE", rel(folder, repo) + "/", "folder has no README.md")
                continue
            linked = {(folder / t.split("#")[0]).resolve() for t in LINK.findall(texts.get(readme, ""))}
            for p in docs:
                if p.parent == folder and p.name != "README.md" and p.resolve() not in linked:
                    r.add("FAIL", "STRUCTURE", rel(p, repo), f"not linked from {rel(readme, repo)}")
                    missing += 1
        if not missing:
            r.add("OK", "STRUCTURE", "", f"{len(docs)} docs, all linked from their folder README")
        return
    index = repo / cfg["index"]["path"]
    if not index.exists():
        r.add("WARN", "STRUCTURE", cfg["index"]["path"], "index file does not exist")
        return
    itext = index.read_text(encoding="utf-8")
    linked = {(index.parent / t.split("#")[0]).resolve() for t in LINK.findall(itext)}
    mentioned = set(re.findall(r"[\w./-]+\.md", itext))
    missing = 0
    for p in docs:
        if p.resolve() == index.resolve():
            continue
        name = rel(p, index.parent) if p.is_relative_to(index.parent) else rel(p, repo)
        if p.resolve() not in linked and name not in mentioned:
            r.add("FAIL", "STRUCTURE", rel(p, repo), f"not listed in {cfg['index']['path']}")
            missing += 1
    if not missing:
        r.add("OK", "STRUCTURE", "", f"{len(docs)} docs, all listed in {cfg['index']['path']}")


def check_links(repo, cfg, files, texts, r: Report):
    bad = total = 0
    anchor_cache: dict[Path, set[str]] = {}
    for p in files:
        clean = strip_code(texts[p])
        for m in LINK.finditer(clean):
            target = m.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):  # http:, mailto:, etc.
                continue
            total += 1
            path_part, _, anchor = target.partition("#")
            dest = (p.parent / path_part).resolve() if path_part else p.resolve()
            where = f"{rel(p, repo)}:{line_of(clean, m.start())}"
            if not dest.exists():
                r.add("FAIL", "LINKS", where, f"link to missing file: {target}")
                bad += 1
                continue
            if anchor and dest.suffix == ".md":
                if dest not in anchor_cache:
                    anchor_cache[dest] = slugs(dest.read_text(encoding="utf-8"))
                if anchor.lower() not in anchor_cache[dest]:
                    r.add("FAIL", "LINKS", where, f"link to missing heading: {target}")
                    bad += 1
    if not bad:
        r.add("OK", "LINKS", "", f"{total} relative links resolve")


def check_ids(repo, cfg, files, texts, r: Report):
    for kind in cfg["ids"]:
        pat = re.compile(kind["pattern"])
        defs: dict[str, list[str]] = defaultdict(list)
        refs: dict[str, list[str]] = defaultdict(list)
        for p in files:
            clean = strip_code(texts[p])
            def_spans = set()
            for d in kind["defined"]:
                for m in re.finditer(d, clean, re.MULTILINE):
                    defs[m.group(1)].append(f"{rel(p, repo)}:{line_of(clean, m.start())}")
                    def_spans.add(m.start(1))
            for m in pat.finditer(clean):
                if m.start() not in def_spans:
                    refs[m.group(0)].append(f"{rel(p, repo)}:{line_of(clean, m.start())}")
        name = kind["name"]
        if not defs and not refs:
            continue
        problems = 0
        for i, where in sorted(defs.items()):
            if len(where) > 1:
                r.add("FAIL", "IDS", where[1], f"{name} {i} defined twice (also {where[0]})")
                problems += 1
        for i, where in sorted(refs.items()):
            if i not in defs:
                r.add("FAIL", "IDS", where[0], f"{name} {i} referenced but never defined"
                      + (f" ({len(where)} references)" if len(where) > 1 else ""))
                problems += 1
        nums = sorted(int(re.sub(r"\D", "", i)) for i in defs)
        if nums:
            gaps = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums))
            if gaps:
                r.add("WARN", "IDS", "", f"{name} numbering gaps: {gaps[:10]}"
                      + (" …" if len(gaps) > 10 else "") + " (fine if deleted; IDs are never reused)")
        if not problems:
            r.add("OK", "IDS", "", f"{len(defs)} {name} IDs defined, {sum(map(len, refs.values()))} references resolve")


def check_frontmatter(repo, cfg, files, texts, r: Report):
    fm = cfg.get("frontmatter") or {}
    globs, required = fm.get("paths") or [], fm.get("required") or []
    if not globs:
        return
    bad = checked = 0
    for p in files:
        path = rel(p, repo)
        if p.name == "README.md" or not matches(path, globs):
            continue
        checked += 1
        meta = frontmatter(texts[p])
        missing = [k for k in required if not meta.get(k)]
        if missing:
            r.add("FAIL", "FRONTMATTER", path, "missing or empty: " + ", ".join(missing))
            bad += 1
    if not bad:
        r.add("OK", "FRONTMATTER", "", f"{checked} docs have {', '.join(required)}")


def check_stale(repo, cfg, files, texts, r: Report):
    today = dt.date.today()
    stale = snapshots = 0
    for p in files:
        meta = frontmatter(texts[p])
        if "stale_after" not in meta:
            continue
        snapshots += 1
        try:
            due = dt.date.fromisoformat(meta["stale_after"])
        except ValueError:
            r.add("FAIL", "STALE", rel(p, repo), f"stale_after is not a date: {meta['stale_after']}")
            continue
        if due < today:
            watch = f"; watch: {meta['watch']}" if meta.get("watch") else ""
            r.add("WARN", "STALE", rel(p, repo),
                  f"past stale_after {due} (verified {meta.get('verified', '?')}){watch}. Re-verify before relying on it")
            stale += 1
    if snapshots and not stale:
        r.add("OK", "STALE", "", f"{snapshots} snapshot docs within their stale_after date")


GROUPS = {
    "STRUCTURE": check_structure,
    "LINKS": check_links,
    "IDS": check_ids,
    "FRONTMATTER": check_frontmatter,
    "STALE": check_stale,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--only", action="append", choices=list(GROUPS), help="run one group; repeatable")
    ap.add_argument("--quiet", action="store_true", help="hide passing checks")
    ap.add_argument("--hook-exit", action="store_true", help="exit 2 on FAIL (Claude Code hooks block only on 2)")
    args = ap.parse_args()

    repo = args.repo.resolve()
    cfg = load_config(repo)
    files = collect(repo, cfg)
    texts = {p: p.read_text(encoding="utf-8", errors="replace") for p in files}
    r = Report(args.quiet)
    for name in args.only or GROUPS:
        GROUPS[name](repo, cfg, files, texts, r)
    print(f"\n{r.counts['FAIL']} FAIL, {r.counts['WARN']} WARN, {r.counts['OK']} OK  ({len(files)} files)")
    if r.counts["FAIL"]:
        return 2 if args.hook_exit else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
