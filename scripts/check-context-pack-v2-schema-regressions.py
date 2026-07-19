#!/usr/bin/env python3
"""Reject empty structured entries while preserving the canonical v2 examples."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "docs/spec/context-pack-v2.schema.json"
EXAMPLE_PATHS = [
    ROOT / "docs/examples/minimal-example/context-pack-v2.yaml",
    ROOT / "docs/examples/common-example/context-pack-v2.yaml",
]
EMPTY_OBJECT_FIXTURE_PATH = ROOT / "scripts/fixtures/context-pack-v2-empty-objects.json"
MALFORMED_FIXTURE_PATH = ROOT / "scripts/fixtures/context-pack-v2-malformed-entries.json"
SEMANTIC_VALIDATOR_PATH = ROOT / "scripts/validate-context-pack.py"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def format_path(parts: list[Any]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def replace_entry(document: dict[str, Any], path: list[str], value: Any) -> None:
    target: Any = document
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = [value]


def load_semantic_validator() -> Any:
    module_name = "context_pack_semantic_validator"
    spec = importlib.util.spec_from_file_location(module_name, SEMANTIC_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load semantic validator: {SEMANTIC_VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    semantic_validator = load_semantic_validator()

    examples = [load_yaml(path) for path in EXAMPLE_PATHS]
    for path, example in zip(EXAMPLE_PATHS, examples):
        errors = list(validator.iter_errors(example))
        if errors:
            first = min(errors, key=lambda error: list(error.absolute_path))
            raise AssertionError(
                f"canonical example failed: {path}: "
                f"{format_path(list(first.absolute_path))}: {first.message}"
            )
        semantic_errors = semantic_validator.validate_context_pack_v2(example)
        if semantic_errors:
            first = semantic_errors[0]
            raise AssertionError(f"canonical semantic lint failed: {path}: {first.path}: {first.message}")

    base = examples[0]
    empty_object_fixtures = load_json(EMPTY_OBJECT_FIXTURE_PATH)
    malformed_fixtures = load_json(MALFORMED_FIXTURE_PATH)
    if not isinstance(empty_object_fixtures, list) or not empty_object_fixtures:
        raise AssertionError("empty-object fixture list must be non-empty")
    if not isinstance(malformed_fixtures, list) or not malformed_fixtures:
        raise AssertionError("malformed fixture list must be non-empty")
    fixtures = [
        *({**fixture, "value": {}} for fixture in empty_object_fixtures),
        *malformed_fixtures,
    ]

    seen_names: set[str] = set()
    for fixture in fixtures:
        name = fixture.get("name")
        path = fixture.get("path")
        if not isinstance(name, str) or not name or not isinstance(path, list) or not path:
            raise AssertionError(f"invalid negative fixture: {fixture!r}")
        if name in seen_names:
            raise AssertionError(f"duplicate negative fixture name: {name}")
        seen_names.add(name)

        candidate = copy.deepcopy(base)
        replace_entry(candidate, path, fixture.get("value"))
        errors = list(validator.iter_errors(candidate))
        expected_prefix = [*path, 0]
        matching = [
            error
            for error in errors
            if list(error.absolute_path)[: len(expected_prefix)] == expected_prefix
        ]
        if not matching:
            raise AssertionError(
                f"invalid structured entry was accepted by JSON Schema for {name}: "
                f"{format_path(expected_prefix)}"
            )
        expected_semantic_path = format_path(expected_prefix)
        semantic_errors = semantic_validator.validate_context_pack_v2(candidate)
        if not any(error.path.startswith(expected_semantic_path) for error in semantic_errors):
            raise AssertionError(
                f"semantic lint accepted invalid structured entry for {name}: "
                f"{expected_semantic_path}"
            )

    print(
        "Context Pack v2 schema regressions passed: "
        f"{len(EXAMPLE_PATHS)} canonical examples, {len(empty_object_fixtures)} empty-object "
        f"negatives, and {len(malformed_fixtures)} malformed negatives through JSON Schema "
        "and semantic lint."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
