#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print("❌ Missing dependency: pyyaml", file=sys.stderr)
    print("   Install: python3 -m pip install -r scripts/requirements-qa.txt", file=sys.stderr)
    raise SystemExit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("❌ Missing dependency: jsonschema", file=sys.stderr)
    print("   Install: python3 -m pip install -r scripts/requirements-qa.txt", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = ROOT / "docs/spec/context-pack-v1.schema.json"


def _is_simple_key(key: str) -> bool:
    if key == "":
        return False
    if key[0].isdigit():
        return False
    return all(ch.isalnum() or ch == "_" for ch in key)


def format_path(parts: Iterable[Any]) -> str:
    out = "$"
    for p in parts:
        if isinstance(p, int):
            out += f"[{p}]"
            continue
        key = str(p)
        if _is_simple_key(key):
            out += f".{key}"
        else:
            out += f"[{json.dumps(key)}]"
    return out


def load_document(file_path: Path) -> Any:
    ext = file_path.suffix.lower()
    if ext not in (".yml", ".yaml", ".json"):
        raise ValueError(f"Unsupported file extension: {ext} (expected .yaml/.yml/.json)")

    with file_path.open("r", encoding="utf-8") as f:
        if ext in (".yml", ".yaml"):
            return yaml.safe_load(f)
        return json.load(f)


def load_schema(schema_path: Path) -> Any:
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Context Pack v1 YAML/JSON with JSON Schema.")
    parser.add_argument("file", help="Target file path (.yaml/.yml/.json)")
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA),
        help=f"Schema file path (default: {DEFAULT_SCHEMA})",
    )
    args = parser.parse_args(argv)

    file_path = Path(args.file)
    schema_path = Path(args.schema)

    try:
        doc = load_document(file_path)
    except Exception as e:
        print(f"❌ Failed to load: {file_path}: {e}", file=sys.stderr)
        return 2

    try:
        schema = load_schema(schema_path)
    except Exception as e:
        print(f"❌ Failed to load schema: {schema_path}: {e}", file=sys.stderr)
        return 2

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:
        print(f"❌ Invalid JSON Schema: {schema_path}: {e}", file=sys.stderr)
        return 2

    validator = Draft202012Validator(schema)
    errors = [(format_path(e.absolute_path), e.message) for e in validator.iter_errors(doc)]

    if errors:
        print(f"❌ Schema validation failed: {file_path}", file=sys.stderr)
        for path, message in sorted(errors, key=lambda x: x[0]):
            print(f"- {path}: {message}", file=sys.stderr)
        return 1

    print(f"✅ Schema validation passed: {file_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
