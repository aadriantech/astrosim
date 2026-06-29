"""Structured LLM insight export."""

from __future__ import annotations

import json
from pathlib import Path

from astrosim.ai.hooks import AIHooks, InsightRequest, LLMClient
from astrosim.engine.simulator import SimulationResult


def export_insight_json(
    result: SimulationResult,
    output_path: str | Path,
    *,
    client: LLMClient | None = None,
    provider: str | None = None,
) -> Path:
    """Write insight payload validated by llm_insight.schema.json."""
    hooks = AIHooks(client)
    content = hooks.generate_insights(InsightRequest(result=result))
    offline = client is None
    payload = {
        "content": content,
        "offline": offline,
        "provider": provider or ("offline" if offline else "custom"),
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2))
    return output