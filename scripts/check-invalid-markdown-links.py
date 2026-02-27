#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    "_site",
    "vendor",
    "node_modules",
    "book-formatter",
    "qa-reports",
}

FENCE_RE = re.compile(r"^\s*```")
INVALID_LINK_RE = re.compile(r"\]\([^)\n]*）")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.is_file():
            files.append(p)
    return sorted(files)


def main() -> int:
    hits: list[tuple[Path, int, str]] = []

    for file_path in iter_markdown_files():
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        in_fence = False
        for lineno, line in enumerate(text.splitlines(), start=1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            if INVALID_LINK_RE.search(line):
                hits.append((file_path, lineno, line))

    if not hits:
        print("✅ No invalid markdown links found.")
        return 0

    print("❌ Invalid markdown links found (full-width '）' inside link URL parentheses):", file=sys.stderr)
    for file_path, lineno, line in hits:
        rel = file_path.relative_to(ROOT)
        print(f"- {rel}:{lineno}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

