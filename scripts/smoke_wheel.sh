#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

pip install -q build
python3 -m build -o dist-wheel-smoke
VENV="/tmp/astrosim-wheel-smoke-$$"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q dist-wheel-smoke/*.whl
"$VENV/bin/astrosim" --help >/dev/null
rm -rf "$VENV" dist-wheel-smoke
echo "Wheel smoke OK"