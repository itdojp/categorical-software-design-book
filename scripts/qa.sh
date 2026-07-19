#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT/qa-reports"
BOOK_FORMATTER_DIR="$ROOT/book-formatter"
BOOK_FORMATTER_REMOTE_URL="${BOOK_FORMATTER_REMOTE_URL:-https://github.com/itdojp/book-formatter.git}"
BOOK_FORMATTER_REF="${BOOK_FORMATTER_REF:-69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c}"

# Keep every relative path used by downstream validators anchored to the repository.
cd "$ROOT"

die() {
  local msg="$1"
  echo "❌ $msg" >&2
  exit 1
}

echo "==> Preparing book-formatter: $BOOK_FORMATTER_DIR"
echo "==> Using book-formatter ref: $BOOK_FORMATTER_REF"
if [[ ! -d "$BOOK_FORMATTER_DIR" ]]; then
  git init "$BOOK_FORMATTER_DIR"
  (
    cd "$BOOK_FORMATTER_DIR"
    git remote add origin "$BOOK_FORMATTER_REMOTE_URL"
    git fetch --depth 1 origin "$BOOK_FORMATTER_REF"
    git checkout --detach FETCH_HEAD
  )
else
  if [[ ! -d "$BOOK_FORMATTER_DIR/.git" ]]; then
    die "book-formatter exists but is not a git repository: $BOOK_FORMATTER_DIR"
  fi
  (
    cd "$BOOK_FORMATTER_DIR"
    if [[ -n "$(git status --porcelain)" ]]; then
      echo "❌ book-formatter has local changes: $BOOK_FORMATTER_DIR" >&2
      echo "   Commit/remove them or delete '$BOOK_FORMATTER_DIR' and run this script again." >&2
      exit 1
    fi
    if git remote get-url origin >/dev/null 2>&1; then
      current_origin="$(git remote get-url origin)"
      if [[ "$current_origin" != "$BOOK_FORMATTER_REMOTE_URL" ]]; then
        echo "==> Resetting book-formatter origin from '$current_origin' to '$BOOK_FORMATTER_REMOTE_URL'"
        git remote set-url origin "$BOOK_FORMATTER_REMOTE_URL"
      fi
    else
      git remote add origin "$BOOK_FORMATTER_REMOTE_URL"
    fi
    if ! git fetch --depth 1 origin "$BOOK_FORMATTER_REF"; then
      echo "❌ Failed to fetch book-formatter ref '$BOOK_FORMATTER_REF' in $BOOK_FORMATTER_DIR" >&2
      echo "   If this problem persists, try removing '$BOOK_FORMATTER_DIR' and run this script again." >&2
      exit 1
    fi
    git checkout --detach FETCH_HEAD
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
missing_py_deps=false
if ! python3 -c "import yaml" >/dev/null 2>&1; then
  missing_py_deps=true
fi
if ! python3 -c "import jsonschema" >/dev/null 2>&1; then
  missing_py_deps=true
fi

if [[ "$missing_py_deps" == "true" ]]; then
  req_file="$ROOT/scripts/requirements-qa.txt"
  if [[ ! -f "$req_file" ]]; then
    die "Python requirements file not found: $req_file"
  fi

  if [[ -n "${VIRTUAL_ENV:-}" || -n "${CONDA_PREFIX:-}" ]]; then
    python3 -m pip install -r "$req_file"
  else
    python3 -m pip install --user -r "$req_file"
  fi
fi

python3 "$ROOT/scripts/check-metadata-consistency.py"
python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/common-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/minimal-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/common-example/context-pack-v2.yaml"
python3 "$ROOT/scripts/validate-context-pack.py" "$ROOT/docs/examples/minimal-example/context-pack-v2.yaml"
python3 "$ROOT/scripts/validate-context-pack-schema.py" "$ROOT/docs/examples/common-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack-schema.py" "$ROOT/docs/examples/minimal-example/context-pack-v1.yaml"
python3 "$ROOT/scripts/validate-context-pack-schema.py" "$ROOT/docs/examples/common-example/context-pack-v2.yaml"
python3 "$ROOT/scripts/validate-context-pack-schema.py" "$ROOT/docs/examples/minimal-example/context-pack-v2.yaml"
python3 "$ROOT/scripts/check-context-pack-minimal-example-sync.py"
python3 "$ROOT/scripts/check-placeholders.py"
python3 "$ROOT/scripts/check-invalid-markdown-links.py"
node "$ROOT/scripts/check-associativity-wording.js"
node "$ROOT/scripts/check-associativity-wording.js" --self-test
node "$ROOT/scripts/check-monad-laws.js"
node "$ROOT/scripts/check-monad-laws.js" --self-test
echo "==> Building rendered HTML (Jekyll)"
if ! command -v bundle >/dev/null 2>&1; then
  die "Bundler is required for rendered HTML checks. Install Ruby/Bundler and run bundle install first."
fi

(
  cd "$ROOT"
  bundle exec jekyll build
)

python3 "$ROOT/scripts/check-rendered-html.py" --site-root "$ROOT/_site"

echo "✅ QA complete. Reports: $REPORT_DIR"
