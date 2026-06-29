#!/usr/bin/env bash
# Opt-in live LLM smoke — skipped when XAI_API_KEY is unset.
set -euo pipefail

if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "SKIP: XAI_API_KEY not set — live LLM smoke skipped"
  exit 0
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src"

python3 - <<'PY'
from astrosim.ai.adapters import GrokLLMClient

client = GrokLLMClient()
result = client.complete("Reply with one word: OK")
assert result and "offline" not in result.lower()
print("Live LLM smoke OK:", result[:80])
PY