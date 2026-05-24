#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate repository metadata used by package, Jekyll, and public book entry points."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ModuleNotFoundError as exc:
    print(
        "❌ PyYAML is required. Install QA dependencies with: "
        "python3 -m pip install -r scripts/requirements-qa.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping: {path}")
    return data


def load_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError(f"Front matter not found: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Expected front matter mapping: {path}")
    return data


def normalize_url(value: Optional[str]) -> str:
    if not value:
        return ""
    value = value.strip()
    if value.startswith("git+"):
        value = value[4:]
    return value.rstrip("/")


def expect_equal(errors: list[str], label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    book = load_json(ROOT / "book-config.json")
    package = load_json(ROOT / "package.json")
    jekyll = load_yaml(ROOT / "_config.yml")
    index = load_front_matter(ROOT / "index.md")

    repo = book["repository"]
    links = book["links"]
    expected_repo_full = f"{repo['owner']}/{repo['name']}"
    expected_pages_url = links["pagesUrl"].rstrip("/")
    expected_repo_url = normalize_url(repo["url"])
    errors: list[str] = []

    # Canonical book identity.
    expect_equal(errors, "package.name", package.get("name"), repo["name"])
    expect_equal(errors, "package.version", package.get("version"), book.get("version"))
    expect_equal(errors, "package.description", package.get("description"), book.get("description"))
    expect_equal(errors, "package.author", package.get("author"), book.get("author"))
    expect_equal(errors, "package.license", package.get("license"), book.get("license"))

    # Published Jekyll metadata.
    expect_equal(errors, "_config.title", jekyll.get("title"), book.get("title"))
    expect_equal(errors, "_config.description", jekyll.get("description"), book.get("description"))
    expect_equal(errors, "_config.author", jekyll.get("author"), book.get("author"))
    expect_equal(errors, "_config.version", jekyll.get("version"), book.get("version"))
    expect_equal(errors, "_config.lang", jekyll.get("lang"), book.get("language"))
    expect_equal(errors, "_config.repository", jekyll.get("repository"), expected_repo_full)
    expect_equal(errors, "_config.repository_branch", jekyll.get("repository_branch"), repo.get("branch"))
    actual_pages_url = f"{jekyll.get('url', '').rstrip('/')}{jekyll.get('baseurl', '')}".rstrip("/")
    expect_equal(errors, "_config url/baseurl", actual_pages_url, expected_pages_url)

    # Public entry page metadata should match the canonical book identity.
    expect_equal(errors, "index front matter title", index.get("title"), book.get("title"))
    expect_equal(errors, "index front matter description", index.get("description"), book.get("description"))

    # npm/GitHub links should point to the same repository and public site.
    package_repo = package.get("repository") or {}
    if not isinstance(package_repo, dict):
        errors.append("package.repository: expected object with type/url")
    else:
        expect_equal(errors, "package.repository.type", package_repo.get("type"), "git")
        expect_equal(
            errors,
            "package.repository.url",
            normalize_url(package_repo.get("url")),
            expected_repo_url,
        )

    expect_equal(errors, "package.homepage", normalize_url(package.get("homepage")), expected_pages_url)

    package_bugs = package.get("bugs") or {}
    if not isinstance(package_bugs, dict):
        errors.append("package.bugs: expected object with url")
    else:
        expect_equal(
            errors,
            "package.bugs.url",
            normalize_url(package_bugs.get("url")),
            normalize_url(links["issuesUrl"]),
        )

    if errors:
        print("❌ Metadata consistency check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("✅ Metadata is consistent across book-config.json, package.json, _config.yml, and index.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
