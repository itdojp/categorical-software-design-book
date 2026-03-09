#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TABLE_RE = re.compile(r"<table\b", re.IGNORECASE)
LINK_HREF_RE = re.compile(r"<a\b[^>]*href=[\"']([^\"']+)[\"']", re.IGNORECASE)
IMG_SRC_RE = re.compile(r"<img\b[^>]*src=[\"']([^\"']+)[\"']", re.IGNORECASE)
CLASS_ATTR_RE = re.compile(r"class=[\"']([^\"']*)[\"']", re.IGNORECASE)


def class_count(html: str, class_name: str) -> int:
    count = 0
    target = class_name.casefold()
    for match in CLASS_ATTR_RE.finditer(html):
        tokens = match.group(1).split()
        if any(token.casefold() == target for token in tokens):
            count += 1
    return count


def has_table(html: str) -> bool:
    return bool(TABLE_RE.search(html))


def has_table_headers(html: str, headers: list[str]) -> bool:
    return all(
        re.search(rf"<th\b[^>]*>\s*{re.escape(header)}\s*</th>", html, re.IGNORECASE)
        for header in headers
    )


def has_link_fragment(html: str, fragment: str) -> bool:
    return any(fragment in href for href in LINK_HREF_RE.findall(html))


def has_img_fragment(html: str, fragment: str) -> bool:
    return any(fragment in src for src in IMG_SRC_RE.findall(html))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check rendered HTML regressions for critical pages.")
    parser.add_argument("--site-root", default="_site", help="Path to Jekyll build output (default: _site)")
    args = parser.parse_args()

    site_root = Path(args.site_root)
    checks = [
        (
            Path("chapters/chapter01/index.html"),
            [
                ("missing <table> for failure patterns", lambda html: has_table(html)),
                (
                    "missing expected headers for failure-pattern table",
                    lambda html: has_table_headers(html, ["失敗パターン", "典型症状", "予防策（設計成果物）"]),
                ),
            ],
        ),
        (
            Path("style/terminology/index.html"),
            [
                ("missing <table> for terminology guide", lambda html: has_table(html)),
                (
                    "missing expected headers for terminology table",
                    lambda html: has_table_headers(html, ["English", "日本語", "備考"]),
                ),
                (
                    "missing rendered internal link to /style/notation/",
                    lambda html: has_link_fragment(html, "/style/notation/"),
                ),
            ],
        ),
        (
            Path("index.html"),
            [
                ("missing Mermaid live wrapper for concept map", lambda html: class_count(html, "mermaid-live") >= 1 and class_count(html, "mermaid-wrapper") >= 1),
                ("missing Mermaid fallback for concept map", lambda html: class_count(html, "mermaid-fallback") >= 1 and has_img_fragment(html, "/assets/images/shared/context-pack-concept-map.svg")),
            ],
        ),
        (
            Path("chapters/chapter01/index.html"),
            [
                ("missing Mermaid live wrapper for chapter01 loop", lambda html: class_count(html, "mermaid-live") >= 1 and class_count(html, "mermaid-wrapper") >= 1),
                ("missing Mermaid fallback for chapter01 loop", lambda html: class_count(html, "mermaid-fallback") >= 1 and has_img_fragment(html, "/assets/images/chapter01/context-pack-loop.svg")),
            ],
        ),
        (
            Path("chapters/chapter04/index.html"),
            [
                ("missing Mermaid live wrapper for chapter04 functor diagram", lambda html: class_count(html, "mermaid-live") >= 1 and class_count(html, "mermaid-wrapper") >= 1),
                ("missing Mermaid fallback for chapter04 functor diagram", lambda html: class_count(html, "mermaid-fallback") >= 1 and has_img_fragment(html, "/assets/images/chapter04/spec-code-functor.svg")),
            ],
        ),
        (
            Path("chapters/chapter07/index.html"),
            [
                ("missing Mermaid live wrappers for chapter07 diagrams", lambda html: class_count(html, "mermaid-live") >= 2 and class_count(html, "mermaid-wrapper") >= 2),
                ("missing Pullback fallback SVG", lambda html: has_img_fragment(html, "/assets/images/chapter07/pullback.svg")),
                ("missing Pushout fallback SVG", lambda html: has_img_fragment(html, "/assets/images/chapter07/pushout.svg")),
            ],
        ),
        (
            Path("chapters/chapter09/index.html"),
            [
                ("missing Mermaid live wrapper for chapter09 effect-boundary diagram", lambda html: class_count(html, "mermaid-live") >= 1 and class_count(html, "mermaid-wrapper") >= 1),
                ("missing Mermaid fallback for chapter09 effect-boundary diagram", lambda html: class_count(html, "mermaid-fallback") >= 1 and has_img_fragment(html, "/assets/images/chapter09/pure-core-impure-shell.svg")),
            ],
        ),
    ]

    errors: list[str] = []
    for relative_path, requirements in checks:
        html_path = site_root / relative_path
        if not html_path.exists():
            errors.append(f"{relative_path}: rendered file not found")
            continue

        html = html_path.read_text(encoding="utf-8")
        for message, predicate in requirements:
            if not predicate(html):
                errors.append(f"{relative_path}: {message}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
