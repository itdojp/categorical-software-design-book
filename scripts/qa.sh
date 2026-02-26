#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT/qa-reports"
BOOK_FORMATTER_DIR="$ROOT/book-formatter"

echo "==> Preparing book-formatter: $BOOK_FORMATTER_DIR"
if [[ ! -d "$BOOK_FORMATTER_DIR" ]]; then
  git clone --depth 1 https://github.com/itdojp/book-formatter.git "$BOOK_FORMATTER_DIR"
else
  if [[ ! -d "$BOOK_FORMATTER_DIR/.git" ]]; then
    echo "❌ book-formatter exists but is not a git repository: $BOOK_FORMATTER_DIR" >&2
    exit 2
  fi
  (
    cd "$BOOK_FORMATTER_DIR"
    git fetch origin
    git checkout main
    git pull --ff-only
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
if ! python3 -c "import yaml" >/dev/null 2>&1; then
  python3 -m pip install --upgrade pip
  python3 -m pip install pyyaml
fi

python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/common-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/minimal-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/check-context-pack-minimal-example-sync.py"
python3 "$ROOT/scripts/check-placeholders.py"

echo "✅ QA complete. Reports: $REPORT_DIR"
