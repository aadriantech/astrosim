"""Contract tests: export_result.schema.json validates export_json output."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.export.formats import export_json
from astrosim.subsystems import DEFAULT_SUBSYSTEMS

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "export_result.schema.json"


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def _run_short_simulation():
    config = SimulationConfig(
        name="export-contract-test",
        duration_hours=12,
        timestep_hours=6,
        crew_count=2,
        parameters={"solar_array_kw": 40, "base_load_kw": 10},
    )
    return Simulator(config, DEFAULT_SUBSYSTEMS).run()


def test_export_json_output_validates_against_schema(tmp_path):
    result = _run_short_simulation()
    path = export_json(result, tmp_path / "results.json")
    data = json.loads(path.read_text())
    jsonschema.validate(data, _load_schema())


def test_minimal_valid_export_with_empty_budgets_and_history():
    data = {
        "config": {
            "name": "minimal",
            "duration_hours": 24,
            "timestep_hours": 1,
            "crew_count": 0,
            "location": "lunar",
            "parameters": {},
        },
        "energy": {},
        "mass": {},
        "reliability": {},
        "history": [],
    }
    jsonschema.validate(data, _load_schema())


def test_reliability_risk_pattern_keys_are_valid():
    data = {
        "config": {
            "name": "risk",
            "duration_hours": 1,
            "timestep_hours": 1,
            "crew_count": 0,
            "location": "mars",
            "parameters": {"solar_array_kw": 10},
        },
        "energy": {"generated_kwh": 1.0, "consumed_kwh": 0.5, "net_kwh": 0.5},
        "mass": {
            "imported_kg": 0.0,
            "produced_kg": 0.0,
            "consumed_kg": 0.0,
            "net_import_kg": 0.0,
        },
        "reliability": {
            "mission_success_probability": 0.99,
            "risk_structure": 0.01,
            "risk_power": 0.0,
        },
        "history": [
            {
                "time_hours": 0,
                "step": 0,
                "mass_kg": 0.0,
                "reliability.cumulative_risk": 0.0,
                "reliability.success_probability": 1.0,
                "power.generated_kwh": 1.0,
            }
        ],
    }
    jsonschema.validate(data, _load_schema())


def test_missing_top_level_key_fails_validation():
    data = {
        "config": {
            "name": "bad",
            "duration_hours": 1,
            "timestep_hours": 1,
            "crew_count": 0,
            "location": "lunar",
            "parameters": {},
        },
        "energy": {},
        "mass": {},
        "reliability": {},
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(data, _load_schema())