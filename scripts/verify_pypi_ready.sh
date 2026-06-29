#!/usr/bin/env bash
# Verify package is PyPI-ready (build + optional install smoke). Does not upload.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if python3 -m venv /tmp/astrosim-venv-probe 2>/dev/null; then
  rm -rf /tmp/astrosim-venv-probe
  bash "$ROOT/scripts/smoke_wheel.sh"
else
  pip install -q build 2>/dev/null || pip install -q build --break-system-packages
  rm -rf dist-pypi-ready
  python3 -m build -o dist-pypi-ready
  pip install -q twine 2>/dev/null || pip install -q twine --break-system-packages
  twine check dist-pypi-ready/*
  rm -rf dist-pypi-ready
  echo "PyPI-ready build OK (wheel install skipped — no python3-venv)"
fi

PYTHONPATH="${ROOT}/src" python3 -c "import astrosim; print(f'version={astrosim.__version__}')"
echo "PyPI-ready verification OK"