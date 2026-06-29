#!/usr/bin/env bash
# System integrity gate — run before Phase 7 or release tags.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="${ROOT}/src"
export MPLBACKEND=Agg

echo "== Agent memory =="
bash scripts/check_agent_sync.sh

echo "== Unit + contract tests (coverage) =="
if ! python3 -c "import pytest, jsonschema, scipy" 2>/dev/null; then
  pip install -q -e ".[dev,optimize]" 2>/dev/null || pip install -q -e ".[dev]" || true
fi
pytest -q --cov=astrosim --cov-fail-under=80

echo "== Example smokes =="
bash scripts/smoke_examples.sh
bash scripts/smoke_custom_subsystem.sh
bash scripts/smoke_mars_quick.sh

echo "== Performance benchmark (report-only) =="
python3 scripts/benchmark_sim.py

echo "== Opt-in LLM smoke =="
bash scripts/smoke_llm.sh

echo "INTEGRITY OK"