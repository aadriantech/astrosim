#!/usr/bin/env bash
# Smoke-test primary example script; asserts expected artifacts exist.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="${ROOT}/src"

OUTPUT="${ROOT}/output/lunar_base"

python3 examples/run_lunar_base.py

for artifact in results.json results.csv dashboard.png dashboard.html; do
  if [[ ! -f "${OUTPUT}/${artifact}" ]]; then
    echo "SMOKE FAILED: missing ${OUTPUT}/${artifact}"
    exit 1
  fi
done

echo "Example smoke OK (${OUTPUT})"