#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


HEADING = "## 最小の有効例（Minimal valid example）"
SYNC_TARGETS = [
    (
        Path("docs/spec/context-pack-v1.md"),
        Path("docs/examples/minimal-example/context-pack-v1.yaml"),
    ),
    (
        Path("docs/spec/context-pack-v2.md"),
        Path("docs/examples/minimal-example/context-pack-v2.yaml"),
    ),
]


def extract_first_yaml_fence_after_heading(markdown: str, heading: str) -> str:
    idx = markdown.find(heading)
    if idx < 0:
        raise ValueError(f"Heading not found: {heading!r}")

    tail = markdown[idx:]
    m = re.search(r"```yaml\s*\n(.*?)\n```", tail, re.DOTALL)
    if not m:
        raise ValueError("YAML code fence not found under the target heading")

    return m.group(1)


def check_pair(spec_md: Path, ssot_yaml: Path) -> int:
    if not spec_md.exists():
        print(f"❌ Spec file not found: {spec_md}", file=sys.stderr)
        return 2
    if not ssot_yaml.exists():
        print(f"❌ SSOT file not found: {ssot_yaml}", file=sys.stderr)
        return 2

    spec_text = spec_md.read_text(encoding="utf-8")
    try:
        snippet_yaml_text = extract_first_yaml_fence_after_heading(spec_text, HEADING)
    except ValueError as e:
        print(f"❌ Failed to extract YAML snippet from spec {spec_md}: {e}", file=sys.stderr)
        return 2

    try:
        snippet_doc = yaml.safe_load(snippet_yaml_text)
    except Exception as e:
        print(f"❌ Failed to parse YAML snippet in spec: {e}", file=sys.stderr)
        return 2

    try:
        ssot_doc = yaml.safe_load(ssot_yaml.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to parse SSOT YAML: {e}", file=sys.stderr)
        return 2

    if snippet_doc != ssot_doc:
        print("❌ Spec minimal example YAML differs from SSOT file.", file=sys.stderr)
        print(f"- Spec: {spec_md}", file=sys.stderr)
        print(f"- SSOT: {ssot_yaml}", file=sys.stderr)
        return 1

    print(f"✅ Spec minimal example YAML is in sync with SSOT: {ssot_yaml}")
    return 0


def main() -> int:
    for spec_md, ssot_yaml in SYNC_TARGETS:
        result = check_pair(spec_md, ssot_yaml)
        if result != 0:
            return result
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
