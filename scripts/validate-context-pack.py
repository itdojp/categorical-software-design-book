#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

import yaml


@dataclass(frozen=True)
class ValidationErrorItem:
    path: str
    message: str


def _is_str_list(v: Any) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


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
    _expect(isinstance(name, str) and name.strip() != "", "$.name", "name は空でない文字列である必要があります", errors)

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
            for i, t in enumerate(terms):
                p = f"$.domain_glossary.terms[{i}]"
                _expect(isinstance(t, dict), p, "term エントリはオブジェクトである必要があります", errors)
                if isinstance(t, dict):
                    _expect(isinstance(t.get("term"), str) and t.get("term").strip() != "", f"{p}.term", "term は空でない文字列である必要があります", errors)
                    _expect(isinstance(t.get("ja"), str) and t.get("ja").strip() != "", f"{p}.ja", "ja は空でない文字列である必要があります", errors)

    objects = doc.get("objects")
    _expect(isinstance(objects, list), "$.objects", "objects は配列である必要があります", errors)
    if isinstance(objects, list):
        for i, o in enumerate(objects):
            p = f"$.objects[{i}]"
            _expect(isinstance(o, dict), p, "object エントリはオブジェクトである必要があります", errors)
            if isinstance(o, dict):
                _expect(isinstance(o.get("id"), str) and o.get("id").strip() != "", f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(isinstance(o.get("kind"), str) and o.get("kind").strip() != "", f"{p}.kind", "kind は空でない文字列である必要があります", errors)
                if "states" in o:
                    _expect(_is_str_list(o.get("states")), f"{p}.states", "states は文字列配列である必要があります", errors)
                if "fields" in o:
                    _expect(_is_str_list(o.get("fields")), f"{p}.fields", "fields は文字列配列である必要があります", errors)

    morphisms = doc.get("morphisms")
    _expect(isinstance(morphisms, list), "$.morphisms", "morphisms は配列である必要があります", errors)
    if isinstance(morphisms, list):
        for i, m in enumerate(morphisms):
            p = f"$.morphisms[{i}]"
            _expect(isinstance(m, dict), p, "morphism エントリはオブジェクトである必要があります", errors)
            if isinstance(m, dict):
                _expect(isinstance(m.get("id"), str) and m.get("id").strip() != "", f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(isinstance(m.get("input"), dict), f"{p}.input", "input はオブジェクトである必要があります", errors)
                _expect(isinstance(m.get("output"), dict), f"{p}.output", "output はオブジェクトである必要があります", errors)
                _expect(_is_str_list(m.get("pre")), f"{p}.pre", "pre は文字列配列である必要があります", errors)
                _expect(_is_str_list(m.get("post")), f"{p}.post", "post は文字列配列である必要があります", errors)
                _expect(_is_str_list(m.get("failures")), f"{p}.failures", "failures は文字列配列である必要があります", errors)

    diagrams = doc.get("diagrams")
    _expect(isinstance(diagrams, list), "$.diagrams", "diagrams は配列である必要があります", errors)
    if isinstance(diagrams, list):
        for i, d in enumerate(diagrams):
            p = f"$.diagrams[{i}]"
            _expect(isinstance(d, dict), p, "diagram エントリはオブジェクトである必要があります", errors)
            if isinstance(d, dict):
                _expect(isinstance(d.get("id"), str) and d.get("id").strip() != "", f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(isinstance(d.get("statement"), str) and d.get("statement").strip() != "", f"{p}.statement", "statement は空でない文字列である必要があります", errors)
                _expect(_is_str_list(d.get("verification")), f"{p}.verification", "verification は文字列配列である必要があります", errors)

    constraints = doc.get("constraints")
    _expect(isinstance(constraints, dict), "$.constraints", "constraints はオブジェクトである必要があります", errors)

    ats = doc.get("acceptance_tests")
    _expect(isinstance(ats, list), "$.acceptance_tests", "acceptance_tests は配列である必要があります", errors)
    if isinstance(ats, list):
        for i, at in enumerate(ats):
            p = f"$.acceptance_tests[{i}]"
            _expect(isinstance(at, dict), p, "acceptance_test エントリはオブジェクトである必要があります", errors)
            if isinstance(at, dict):
                _expect(isinstance(at.get("id"), str) and at.get("id").strip() != "", f"{p}.id", "id は空でない文字列である必要があります", errors)
                _expect(isinstance(at.get("scenario"), str) and at.get("scenario").strip() != "", f"{p}.scenario", "scenario は空でない文字列である必要があります", errors)
                _expect(_is_str_list(at.get("expected")), f"{p}.expected", "expected は文字列配列である必要があります", errors)

    cc = doc.get("coding_conventions")
    _expect(isinstance(cc, dict), "$.coding_conventions", "coding_conventions はオブジェクトである必要があります", errors)
    if isinstance(cc, dict):
        _expect(isinstance(cc.get("language"), str), "$.coding_conventions.language", "language は文字列である必要があります", errors)
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

