#!/usr/bin/env bash
# Verify distributed AGENT.md memory exists for each code domain.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REQUIRED=(
  "AGENTS.md"
  "AGENT_INDEX.md"
  "src/astrosim/AGENT.md"
  "src/astrosim/engine/AGENT.md"
  "src/astrosim/subsystems/AGENT.md"
  "src/astrosim/budgeting/AGENT.md"
  "src/astrosim/ai/AGENT.md"
  "src/astrosim/analysis/AGENT.md"
  "src/astrosim/export/AGENT.md"
  "src/astrosim/visualization/AGENT.md"
  "tests/AGENT.md"
  "scenarios/AGENT.md"
  "examples/AGENT.md"
  ".github/AGENT.md"
  "contracts/README.md"
)

missing=0
for f in "${REQUIRED[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "Agent memory check FAILED"
  exit 1
fi

echo "Agent memory check OK (${#REQUIRED[@]} files)"