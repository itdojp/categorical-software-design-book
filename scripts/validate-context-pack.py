#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Optional

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


def _is_list(v: Any) -> bool:
    return isinstance(v, list)


def _is_str_or_object_list(v: Any) -> bool:
    return isinstance(v, list) and all(_is_non_empty_str(x) or isinstance(x, dict) for x in v)


def _is_allowed_tool_contract(v: Any) -> bool:
    if _is_non_empty_str(v):
        return True
    if not isinstance(v, dict):
        return False
    required = ["name", "protocol", "effect", "input_schema_ref", "output_schema_ref"]
    return all(_is_non_empty_str(v.get(key)) for key in required)


def _is_forbidden_tool_contract(v: Any) -> bool:
    if _is_non_empty_str(v):
        return True
    if not isinstance(v, dict):
        return False
    return _is_non_empty_str(v.get("name"))


def _is_allowed_tool_list(v: Any) -> bool:
    return isinstance(v, list) and all(_is_allowed_tool_contract(x) for x in v)


def _is_forbidden_tool_list(v: Any) -> bool:
    return isinstance(v, list) and all(_is_forbidden_tool_contract(x) for x in v)


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


def _expect_object_with_required_keys(
    doc: dict[str, Any],
    key: str,
    required: list[tuple[str, str]],
    errors: list[ValidationErrorItem],
) -> Optional[dict[str, Any]]:
    value = doc.get(key)
    _expect(isinstance(value, dict), f"$.{key}", f"{key} はオブジェクトである必要があります", errors)
    if not isinstance(value, dict):
        return None

    for child, kind in required:
        path = f"$.{key}.{child}"
        child_value = value.get(child)
        if kind == "array":
            _expect(_is_list(child_value), path, f"{child} は配列である必要があります", errors)
        elif kind == "str_array":
            _expect(_is_str_list(child_value), path, f"{child} は文字列配列である必要があります", errors)
        elif kind == "str_or_object_array":
            _expect(
                _is_str_or_object_list(child_value),
                path,
                f"{child} は非空文字列またはオブジェクトの配列である必要があります",
                errors,
            )
        elif kind == "allowed_tool_array":
            _expect(
                _is_allowed_tool_list(child_value),
                path,
                f"{child} は非空文字列、または name/protocol/effect/input_schema_ref/output_schema_ref を持つ tool contract の配列である必要があります",
                errors,
            )
        elif kind == "forbidden_tool_array":
            _expect(
                _is_forbidden_tool_list(child_value),
                path,
                f"{child} は非空文字列、または name を持つ禁止 tool contract の配列である必要があります",
                errors,
            )
        elif kind == "object":
            _expect(isinstance(child_value, dict), path, f"{child} はオブジェクトである必要があります", errors)
        else:
            raise ValueError(f"Unknown validation kind: {kind}")
    return value


def _is_non_empty_rule(value: Any) -> bool:
    return _is_non_empty_str(value) or (isinstance(value, list) and len(value) > 0 and _is_str_list(value))


def _validate_v2_structured_entries(doc: dict[str, Any], errors: list[ValidationErrorItem]) -> None:
    """Semantic lint for the intentionally shallow v2 structured-entry contract."""

    def entries(section: str, field: str) -> list[Any]:
        section_value = doc.get(section)
        if not isinstance(section_value, dict):
            return []
        value = section_value.get(field)
        return value if isinstance(value, list) else []

    def require_string(item: dict[str, Any], key: str, path: str) -> None:
        _expect(_is_non_empty_str(item.get(key)), f"{path}.{key}", f"{key} は空でない文字列である必要があります", errors)

    id_only_fields = [
        ("data_contracts", "schemas"),
        ("open_systems", "components"),
        ("open_systems", "boundaries"),
        ("open_systems", "composition"),
    ]
    for section, field in id_only_fields:
        for index, item in enumerate(entries(section, field)):
            path = f"$.{section}.{field}[{index}]"
            if _is_non_empty_str(item):
                continue
            _expect(isinstance(item, dict), path, "非空文字列または構造化オブジェクトである必要があります", errors)
            if isinstance(item, dict):
                require_string(item, "id", path)

    for index, item in enumerate(entries("data_contracts", "mappings")):
        path = f"$.data_contracts.mappings[{index}]"
        if _is_non_empty_str(item):
            continue
        _expect(isinstance(item, dict), path, "非空文字列またはmappingオブジェクトである必要があります", errors)
        if isinstance(item, dict):
            require_string(item, "id", path)
            endpoints = (
                _is_non_empty_str(item.get("source")) and _is_non_empty_str(item.get("target"))
            ) or (_is_non_empty_str(item.get("from")) and _is_non_empty_str(item.get("to")))
            _expect(endpoints, path, "source/targetまたはfrom/toの非空endpointが必要です", errors)

    for index, item in enumerate(entries("data_contracts", "migration_verification")):
        path = f"$.data_contracts.migration_verification[{index}]"
        if _is_non_empty_str(item):
            continue
        _expect(isinstance(item, dict), path, "非空文字列またはverificationオブジェクトである必要があります", errors)
        if isinstance(item, dict):
            require_string(item, "type", path)

    for index, item in enumerate(entries("views", "lenses_or_optics")):
        path = f"$.views.lenses_or_optics[{index}]"
        if _is_non_empty_str(item):
            continue
        _expect(isinstance(item, dict), path, "非空文字列またはview/opticオブジェクトである必要があります", errors)
        if isinstance(item, dict):
            require_string(item, "id", path)
            require_string(item, "source", path)
            focus = item.get("focus")
            has_view_or_focus = _is_non_empty_str(item.get("view")) or _is_non_empty_str(focus) or (
                isinstance(focus, list) and len(focus) > 0 and _is_str_list(focus)
            )
            _expect(has_view_or_focus, path, "非空のviewまたはfocusが必要です", errors)

    for index, item in enumerate(entries("effects", "operations")):
        path = f"$.effects.operations[{index}]"
        if _is_non_empty_str(item):
            continue
        _expect(isinstance(item, dict), path, "非空文字列またはeffect operationオブジェクトである必要があります", errors)
        if isinstance(item, dict):
            require_string(item, "id", path)
            require_string(item, "kind", path)

    for index, item in enumerate(entries("effects", "handlers")):
        path = f"$.effects.handlers[{index}]"
        if _is_non_empty_str(item):
            continue
        _expect(isinstance(item, dict), path, "非空文字列またはeffect handlerオブジェクトである必要があります", errors)
        if isinstance(item, dict):
            require_string(item, "id", path)
            handles = item.get("handles")
            has_operation = _is_non_empty_str(item.get("operation")) or (
                isinstance(handles, list) and len(handles) > 0 and _is_str_list(handles)
            )
            _expect(has_operation, path, "非空のoperationまたはhandlesが必要です", errors)

    for index, item in enumerate(entries("resource_constraints", "linear_resources")):
        path = f"$.resource_constraints.linear_resources[{index}]"
        if _is_non_empty_str(item):
            continue
        _expect(isinstance(item, dict), path, "非空文字列またはlinear resourceオブジェクトである必要があります", errors)
        if isinstance(item, dict):
            require_string(item, "id", path)
            _expect(_is_non_empty_rule(item.get("rule")), f"{path}.rule", "ruleは非空文字列または非空文字列配列である必要があります", errors)


def validate_context_pack_v2(doc: Any) -> list[ValidationErrorItem]:
    errors = validate_context_pack_v1(doc)

    _expect(isinstance(doc, dict), "$", "トップレベルはオブジェクト（dict）である必要があります", errors)
    if not isinstance(doc, dict):
        return errors

    _expect(doc.get("version") == 2, "$.version", "v2 では version は 2 である必要があります", errors)
    _expect(
        doc.get("context_pack_version") == 2,
        "$.context_pack_version",
        "context_pack_version は 2 である必要があります",
        errors,
    )

    _expect_object_with_required_keys(
        doc,
        "data_contracts",
        [
            ("schemas", "array"),
            ("mappings", "array"),
            ("migration_verification", "str_or_object_array"),
        ],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "open_systems",
        [
            ("components", "array"),
            ("boundaries", "array"),
            ("composition", "array"),
        ],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "views",
        [("lenses_or_optics", "array")],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "effects",
        [
            ("operations", "array"),
            ("handlers", "array"),
            ("effect_safety_notes", "str_array"),
        ],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "agent_runtime",
        [
            ("allowed_tools", "allowed_tool_array"),
            ("forbidden_tools", "forbidden_tool_array"),
            ("guardrails", "object"),
            ("trace_evidence", "object"),
        ],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "resource_constraints",
        [
            ("tool_budget", "object"),
            ("data_sensitivity", "object"),
            ("linear_resources", "array"),
        ],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "change_semantics",
        [
            ("allowed_refactors", "str_array"),
            ("forbidden_conflict_resolutions", "str_array"),
            ("merge_invariants", "str_array"),
        ],
        errors,
    )
    _expect_object_with_required_keys(
        doc,
        "formalization_level",
        [
            ("metaphor_only", "str_array"),
            ("machine_checked", "str_array"),
            ("tested_by_ci", "str_array"),
            ("reviewed_manually", "str_array"),
        ],
        errors,
    )

    _validate_v2_structured_entries(doc, errors)

    return errors


def detect_context_pack_version(doc: Any) -> int:
    if isinstance(doc, dict) and (doc.get("context_pack_version") == 2 or doc.get("version") == 2):
        return 2
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Context Pack v1/v2 YAML/JSON (minimal lint).")
    parser.add_argument("file", help="Target file path (.yaml/.yml/.json)")
    args = parser.parse_args(argv)

    try:
        doc = load_document(args.file)
    except Exception as e:
        print(f"❌ Failed to load: {args.file}: {e}", file=sys.stderr)
        return 2

    context_pack_version = detect_context_pack_version(doc)
    if context_pack_version == 2:
        errors = validate_context_pack_v2(doc)
    else:
        errors = validate_context_pack_v1(doc)
    if errors:
        print(f"❌ Invalid Context Pack v{context_pack_version}: {args.file}", file=sys.stderr)
        for item in errors:
            print(f"- {item.path}: {item.message}", file=sys.stderr)
        return 1

    print(f"✅ Context Pack v{context_pack_version} is valid: {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
