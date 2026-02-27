#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT/qa-reports"
BOOK_FORMATTER_DIR="$ROOT/book-formatter"

die() {
  local msg="$1"
  echo "❌ $msg" >&2
  exit 1
}

echo "==> Preparing book-formatter: $BOOK_FORMATTER_DIR"
if [[ ! -d "$BOOK_FORMATTER_DIR" ]]; then
  git clone --depth 1 https://github.com/itdojp/book-formatter.git "$BOOK_FORMATTER_DIR"
else
  if [[ ! -d "$BOOK_FORMATTER_DIR/.git" ]]; then
    die "book-formatter exists but is not a git repository: $BOOK_FORMATTER_DIR"
  fi
  (
    cd "$BOOK_FORMATTER_DIR"
    if ! git fetch origin; then
      echo "❌ Failed to fetch updates for book-formatter in $BOOK_FORMATTER_DIR" >&2
      echo "   If this problem persists, try removing '$BOOK_FORMATTER_DIR' and run this script again." >&2
      exit 1
    fi
    if ! git checkout main; then
      echo "❌ Failed to switch book-formatter to 'main' branch in $BOOK_FORMATTER_DIR" >&2
      echo "   Ensure the repository is clean or remove '$BOOK_FORMATTER_DIR' and run this script again." >&2
      exit 1
    fi
    if ! git pull --ff-only; then
      echo "❌ Failed to fast-forward book-formatter to the latest 'main' from origin in $BOOK_FORMATTER_DIR" >&2
      echo "   This can happen if there are local changes or the branch has diverged." >&2
      echo "   To fix this, remove '$BOOK_FORMATTER_DIR' and run this script again to reclone book-formatter." >&2
      exit 1
    fi
  )
fi

echo "==> Installing book-formatter dependencies"
(
  cd "$BOOK_FORMATTER_DIR"
  npm ci
)

mkdir -p "$REPORT_DIR"

echo "==> Running quality checks (book-formatter)"
(
  cd "$BOOK_FORMATTER_DIR"

  npm run check-links -- "$ROOT" --output "$REPORT_DIR/link-report.json"
  npm run check-unicode -- "$ROOT" --output "$REPORT_DIR/unicode-report.json"
  npm run check-layout-risk -- "$ROOT" --output "$REPORT_DIR/layout-risk-report.json"
  npm run check-markdown-structure -- "$ROOT" --output "$REPORT_DIR/markdown-structure-report.json"

  npm run check-textlint -- "$ROOT" --output "$REPORT_DIR/textlint-report.json" --fail-on error
  npm run check-textlint -- "$ROOT" --with-preset --output "$REPORT_DIR/textlint-report-with-preset.json" --fail-on none
)

echo "==> Running Context Pack checks (Python)"
missing_pkgs=()
if ! python3 -c "import yaml" >/dev/null 2>&1; then
  missing_pkgs+=("pyyaml")
fi
if ! python3 -c "import jsonschema" >/dev/null 2>&1; then
  missing_pkgs+=("jsonschema")
fi

if ((${#missing_pkgs[@]})); then
  if [[ -n "${VIRTUAL_ENV:-}" || -n "${CONDA_PREFIX:-}" ]]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install "${missing_pkgs[@]}"
  else
    python3 -m pip install --user "${missing_pkgs[@]}"
  fi
fi

python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/common-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/minimal-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack-schema.py" "$ROOT/docs/examples/common-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack-schema.py" "$ROOT/docs/examples/minimal-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/check-context-pack-minimal-example-sync.py"
python3 "$ROOT/scripts/check-placeholders.py"

echo "✅ QA complete. Reports: $REPORT_DIR"
