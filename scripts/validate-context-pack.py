#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

try:
    import yaml
except ImportError:
    print("❌ Missing dependency: pyyaml", file=sys.stderr)
    print("   Install: python3 -m pip install -r scripts/requirements-qa.txt", file=sys.stderr)
    raise SystemExit(2)


@dataclass(frozen=True)
class ValidationErrorItem:
    path: str
    message: str


def _is_non_empty_str(v: Any) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is_str_list(v: Any) -> bool:
    return isinstance(v, list) and all(_is_non_empty_str(x) for x in v)


def _expect(cond: bool, path: str, message: str, errors: list[ValidationErrorItem]) -> None:
    if not cond:
        errors.append(ValidationErrorItem(path=path, message=message))


def load_document(file_path: str) -> Any:
    ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, "r", encoding="utf-8") as f:
        if ext in (".yml", ".yaml"):
            return yaml.safe_load(f)
        if ext == ".json":
            return json.load(f)
    raise ValueError(f"Unsupported file extension: {ext} (expected .yaml/.yml/.json)")


def _check_unique_ids(items: Any, id_key: str, path: str, errors: list[ValidationErrorItem]) -> dict[str, int]:
    if not isinstance(items, list):
        return {}

    seen: dict[str, int] = {}
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        raw = item.get(id_key)
        if not _is_non_empty_str(raw):
            continue
        if raw in seen:
            errors.append(
                ValidationErrorItem(
                    path=f"{path}[{i}].{id_key}",
                    message=f"{id_key} が重複しています（先頭: {path}[{seen[raw]}].{id_key}）",
                )
            )
        else:
            seen[raw] = i
    return seen


def _check_io_field_types(io_obj: Any, path: str, errors: list[ValidationErrorItem]) -> None:
    if not isinstance(io_obj, dict):
        return
    for key, value in io_obj.items():
        if not _is_non_empty_str(key):
            errors.append(ValidationErrorItem(path=path, message="input/output のキーは空でない文字列である必要があります"))
            continue
        if not _is_non_empty_str(value):
            errors.append(
                ValidationErrorItem(
                    path=f"{path}.{key}",
                    message="input/output のフィールド型は空でない文字列である必要があります",
                )
            )


def validate_context_pack_v1(doc: Any) -> list[ValidationErrorItem]:
    errors: list[ValidationErrorItem] = []

    _expect(isinstance(doc, dict), "$", "トップレベルはオブジェクト（dict）である必要があります", errors)
    if not isinstance(doc, dict):
        return errors

    required_top = [
        "version",
        "name",
        "problem_statement",
        "domain_glossary",
        "objects",
        "morphisms",
        "diagrams",
        "constraints",
        "acceptance_tests",
        "coding_conventions",
        "forbidden_changes",
    ]
    for key in required_top:
        _expect(key in doc, f"$.{key}", "必須フィールドが欠落しています", errors)

    version = doc.get("version")
    _expect(isinstance(version, int) and version >= 1, "$.version", "version は 1 以上の整数である必要があります", errors)

    name = doc.get("name")
    _expect(_is_non_empty_str(name), "$.name", "name は空でない文字列である必要があります", errors)

    ps = doc.get("problem_statement")
    _expect(isinstance(ps, dict), "$.problem_statement", "problem_statement はオブジェクトである必要があります", errors)
    if isinstance(ps, dict):
        _expect(_is_str_list(ps.get("goals")), "$.problem_statement.goals", "goals は文字列配列である必要があります", errors)
        _expect(_is_str_list(ps.get("non_goals")), "$.problem_statement.non_goals", "non_goals は文字列配列である必要があります", errors)

    glossary = doc.get("domain_glossary")
    _expect(isinstance(glossary, dict), "$.domain_glossary", "domain_glossary はオブジェクトである必要があります", errors)
    if isinstance(glossary, dict):
        terms = glossary.get("terms")
        _expect(isinstance(terms, list), "$.domain_glossary.terms", "terms は配列である必要があります", errors)
        if isinstance(terms, list):
            _check_unique_ids(terms, "term", "$.domain_glossary.terms", errors)
            for i, t in enumerate(terms):
                p = f"$.domain_glossary.terms[{i}]"
                _expect(isinstance(t, dict), p, "term エントリはオブジェクトである必要があります", errors)
                if isinstance(t, dict):
                    _expect(_is_non_empty_str(t.get("term")), f"{p}.term", "term は空でない文字列である必要があります", errors)
                    _expect(_is_non_empty_str(t.get("ja")), f"{p}.ja", "ja は空でない文字列である必要があります", errors)

    objects = doc.get("objects")
    _expect(isinstance(objects, list), "$.objects", "objects は配列である必要があります", errors)
    if isinstance(objects, list):
        object_id_index = _check_unique_ids(objects, "id", "$.objects", errors)
        for i, o in enumerate(objects):
            p = f"$.objects[{i}]"
            _expect(isinstance(o, dict), p, "object エントリはオブジェクトである必要があります", errors)
            if isinstance(o, dict):
                _expect(_is_non_empty_str(o.get("id")), f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(_is_non_empty_str(o.get("kind")), f"{p}.kind", "kind は空でない文字列である必要があります", errors)
                if "states" in o:
                    _expect(_is_str_list(o.get("states")), f"{p}.states", "states は文字列配列である必要があります", errors)
                if "fields" in o:
                    _expect(_is_str_list(o.get("fields")), f"{p}.fields", "fields は文字列配列である必要があります", errors)

    morphisms = doc.get("morphisms")
    _expect(isinstance(morphisms, list), "$.morphisms", "morphisms は配列である必要があります", errors)
    if isinstance(morphisms, list):
        _check_unique_ids(morphisms, "id", "$.morphisms", errors)
        for i, m in enumerate(morphisms):
            p = f"$.morphisms[{i}]"
            _expect(isinstance(m, dict), p, "morphism エントリはオブジェクトである必要があります", errors)
            if isinstance(m, dict):
                _expect(_is_non_empty_str(m.get("id")), f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(isinstance(m.get("input"), dict), f"{p}.input", "input はオブジェクトである必要があります", errors)
                _expect(isinstance(m.get("output"), dict), f"{p}.output", "output はオブジェクトである必要があります", errors)
                _expect(_is_str_list(m.get("pre")), f"{p}.pre", "pre は文字列配列である必要があります", errors)
                _expect(_is_str_list(m.get("post")), f"{p}.post", "post は文字列配列である必要があります", errors)
                _expect(_is_str_list(m.get("failures")), f"{p}.failures", "failures は文字列配列である必要があります", errors)
                _check_io_field_types(m.get("input"), f"{p}.input", errors)
                _check_io_field_types(m.get("output"), f"{p}.output", errors)

    diagrams = doc.get("diagrams")
    _expect(isinstance(diagrams, list), "$.diagrams", "diagrams は配列である必要があります", errors)
    if isinstance(diagrams, list):
        diagram_id_index = _check_unique_ids(diagrams, "id", "$.diagrams", errors)
        for i, d in enumerate(diagrams):
            p = f"$.diagrams[{i}]"
            _expect(isinstance(d, dict), p, "diagram エントリはオブジェクトである必要があります", errors)
            if isinstance(d, dict):
                _expect(_is_non_empty_str(d.get("id")), f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(_is_non_empty_str(d.get("statement")), f"{p}.statement", "statement は空でない文字列である必要があります", errors)
                _expect(_is_str_list(d.get("verification")), f"{p}.verification", "verification は文字列配列である必要があります", errors)

                involved = d.get("involved")
                if involved is not None:
                    _expect(isinstance(involved, dict), f"{p}.involved", "involved はオブジェクトである必要があります", errors)
                if isinstance(involved, dict):
                    if "objects" in involved:
                        objs = involved.get("objects")
                        _expect(_is_str_list(objs), f"{p}.involved.objects", "objects は文字列配列である必要があります", errors)
                        if isinstance(objs, list) and isinstance(objects, list):
                            for j, oid in enumerate(objs):
                                if oid not in object_id_index:
                                    errors.append(
                                        ValidationErrorItem(
                                            path=f"{p}.involved.objects[{j}]",
                                            message="objects に存在しない Object id が参照されています",
                                        )
                                    )
                    if "morphisms" in involved:
                        ms = involved.get("morphisms")
                        _expect(_is_str_list(ms), f"{p}.involved.morphisms", "morphisms は文字列配列である必要があります", errors)
                        if isinstance(ms, list) and isinstance(morphisms, list):
                            morphism_ids = {m.get("id") for m in morphisms if isinstance(m, dict) and _is_non_empty_str(m.get("id"))}
                            for j, mid in enumerate(ms):
                                if mid not in morphism_ids:
                                    errors.append(
                                        ValidationErrorItem(
                                            path=f"{p}.involved.morphisms[{j}]",
                                            message="morphisms に存在しない Morphism id が参照されています",
                                        )
                                    )

    constraints = doc.get("constraints")
    _expect(isinstance(constraints, dict), "$.constraints", "constraints はオブジェクトである必要があります", errors)

    ats = doc.get("acceptance_tests")
    _expect(isinstance(ats, list), "$.acceptance_tests", "acceptance_tests は配列である必要があります", errors)
    if isinstance(ats, list):
        _check_unique_ids(ats, "id", "$.acceptance_tests", errors)
        for i, at in enumerate(ats):
            p = f"$.acceptance_tests[{i}]"
            _expect(isinstance(at, dict), p, "acceptance_test エントリはオブジェクトである必要があります", errors)
            if isinstance(at, dict):
                _expect(_is_non_empty_str(at.get("id")), f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(_is_non_empty_str(at.get("scenario")), f"{p}.scenario", "scenario は空でない文字列である必要があります", errors)
                _expect(_is_str_list(at.get("expected")), f"{p}.expected", "expected は文字列配列である必要があります", errors)

    cc = doc.get("coding_conventions")
    _expect(isinstance(cc, dict), "$.coding_conventions", "coding_conventions はオブジェクトである必要があります", errors)
    if isinstance(cc, dict):
        _expect(_is_non_empty_str(cc.get("language")), "$.coding_conventions.language", "language は空でない文字列である必要があります", errors)
        _expect(_is_str_list(cc.get("directory")), "$.coding_conventions.directory", "directory は文字列配列である必要があります", errors)
        _expect(isinstance(cc.get("dependencies"), dict), "$.coding_conventions.dependencies", "dependencies はオブジェクトである必要があります", errors)

    fc = doc.get("forbidden_changes")
    _expect(_is_str_list(fc), "$.forbidden_changes", "forbidden_changes は文字列配列である必要があります", errors)

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Context Pack v1 YAML/JSON (minimal lint).")
    parser.add_argument("file", help="Target file path (.yaml/.yml/.json)")
    args = parser.parse_args(argv)

    try:
        doc = load_document(args.file)
    except Exception as e:
        print(f"❌ Failed to load: {args.file}: {e}", file=sys.stderr)
        return 2

    errors = validate_context_pack_v1(doc)
    if errors:
        print(f"❌ Invalid Context Pack v1: {args.file}", file=sys.stderr)
        for item in errors:
            print(f"- {item.path}: {item.message}", file=sys.stderr)
        return 1

    print(f"✅ Context Pack v1 is valid: {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
