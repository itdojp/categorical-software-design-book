#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


SPEC_MD = Path("docs/spec/context-pack-v1.md")
SSOT_YAML = Path("docs/examples/minimal-example/context-pack-v1.yaml")
HEADING = "## 最小の有効例（Minimal valid example）"


def extract_first_yaml_fence_after_heading(markdown: str, heading: str) -> str:
    idx = markdown.find(heading)
    if idx < 0:
        raise ValueError(f"Heading not found: {heading!r}")

    tail = markdown[idx:]
    m = re.search(r"```yaml\s*\n(.*?)\n```", tail, re.DOTALL)
    if not m:
        raise ValueError("YAML code fence not found under the target heading")

    return m.group(1)


def main() -> int:
    if not SPEC_MD.exists():
        print(f"❌ Spec file not found: {SPEC_MD}", file=sys.stderr)
        return 2
    if not SSOT_YAML.exists():
        print(f"❌ SSOT file not found: {SSOT_YAML}", file=sys.stderr)
        return 2

    spec_text = SPEC_MD.read_text(encoding="utf-8")
    try:
        snippet_yaml_text = extract_first_yaml_fence_after_heading(spec_text, HEADING)
    except ValueError as e:
        print(f"❌ Failed to extract YAML snippet from spec: {e}", file=sys.stderr)
        return 2

    try:
        snippet_doc = yaml.safe_load(snippet_yaml_text)
    except Exception as e:
        print(f"❌ Failed to parse YAML snippet in spec: {e}", file=sys.stderr)
        return 2

    try:
        ssot_doc = yaml.safe_load(SSOT_YAML.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to parse SSOT YAML: {e}", file=sys.stderr)
        return 2

    if snippet_doc != ssot_doc:
        print("❌ Spec minimal example YAML differs from SSOT file.", file=sys.stderr)
        print(f"- Spec: {SPEC_MD}", file=sys.stderr)
        print(f"- SSOT: {SSOT_YAML}", file=sys.stderr)
        return 1

    print(f"✅ Spec minimal example YAML is in sync with SSOT: {SSOT_YAML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

