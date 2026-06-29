#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! python3 -c "import mkdocs" 2>/dev/null; then
  pip install -q -e ".[docs]" 2>/dev/null || pip install -q "mkdocs>=1.6" "mkdocs-material>=9.5"
fi

mkdocs build -d site
test -f site/index.html
echo "Docs build OK (site/)"