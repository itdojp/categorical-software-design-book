#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    ROOT / "index.md",
    ROOT / "GLOSSARY.md",
]

GLOBS = [
    ROOT / "chapters/**/*.md",
    ROOT / "appendices/**/*.md",
    ROOT / "docs/**/*.md",
    ROOT / "docs/examples/**/*.*",
]

ALLOWED_EXAMPLE_EXTS = {".yml", ".yaml", ".json"}

ALLOWLIST_FILE = ROOT / ".book-formatter/placeholder-allowlist.txt"

PATTERN = re.compile(
    r"\b(?:TBD|TODO|FIXME|WIP)\b|執筆中|準備中|未作成|後続タスク",
    flags=re.IGNORECASE,
)


def load_allowlist() -> set[Path]:
    if not ALLOWLIST_FILE.exists():
        return set()

    allow: set[Path] = set()
    for raw in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line == "" or line.startswith("#"):
            continue
        allow.add((ROOT / line).resolve())
    return allow


def iter_files() -> Iterable[Path]:
    for p in TARGETS:
        if p.exists():
            yield p

    for g in GLOBS:
        # Path.glob accepts "**" patterns relative to the base path,
        # but we keep absolute roots for clarity.
        for p in ROOT.glob(str(g.relative_to(ROOT))):
            if not p.is_file():
                continue
            if p.suffix.lower() in (".md",):
                yield p
                continue
            if p.suffix.lower() in ALLOWED_EXAMPLE_EXTS:
                yield p


def main() -> int:
    allowlist = load_allowlist()

    hits: list[tuple[Path, int, str]] = []
    for file_path in sorted({p.resolve() for p in iter_files()}):
        if file_path in allowlist:
            continue

        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Treat non-UTF-8 files as out of scope for placeholder checks.
            continue

        for lineno, line in enumerate(text.splitlines(), start=1):
            if PATTERN.search(line):
                hits.append((file_path, lineno, line))

    if not hits:
        print("✅ No placeholders found.")
        return 0

    print("❌ Placeholders found:", file=sys.stderr)
    for file_path, lineno, line in hits:
        rel = file_path.relative_to(ROOT)
        print(f"- {rel}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

