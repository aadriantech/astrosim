"""Tests for structured insight export."""

import json
from pathlib import Path

import jsonschema

from astrosim.ai.insights import export_insight_json
from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import DEFAULT_SUBSYSTEMS

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "llm_insight.schema.json"


class _MockClient:
    def complete(self, prompt: str) -> str:
        return "mock insight"


def test_export_insight_json_offline(tmp_path):
    config = SimulationConfig(
        name="insight-test",
        duration_hours=6,
        timestep_hours=6,
        crew_count=2,
        parameters={"solar_array_kw": 30, "base_load_kw": 8},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
    path = export_insight_json(result, tmp_path / "insight.json")
    payload = json.loads(path.read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
    assert payload["offline"] is True
    assert payload["content"]


def test_export_insight_json_with_mock_client(tmp_path):
    config = SimulationConfig(
        name="insight-mock",
        duration_hours=6,
        timestep_hours=6,
        crew_count=1,
        parameters={"solar_array_kw": 20, "base_load_kw": 5},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
    path = export_insight_json(
        result,
        tmp_path / "insight.json",
        client=_MockClient(),
        provider="mock",
    )
    payload = json.loads(path.read_text())
    assert payload["offline"] is False
    assert payload["provider"] == "mock"
    assert payload["content"] == "mock insight"