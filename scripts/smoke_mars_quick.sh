#!/usr/bin/env bash
# Fast Mars Monte Carlo smoke (5 runs).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src"

python3 - <<'PY'
from pathlib import Path
from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.scenario import build_simulator, load_scenario

root = Path(".")
config = load_scenario(root / "scenarios" / "mars_habitat.yaml")
mc = MonteCarloRunner(base_config=config, build_simulator=build_simulator, seed=1)
result = mc.run(num_runs=5, perturbation=0.05)
assert result.num_runs == 5
assert result.summary
print("Mars quick MC smoke OK")
PY