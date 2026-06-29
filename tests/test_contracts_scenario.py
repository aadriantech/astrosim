"""Contract tests: scenario.schema.json validates canonical scenarios."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "scenario.schema.json"


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def _load_scenario_dict(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def test_lunar_yaml_validates_against_scenario_schema():
    data = _load_scenario_dict(ROOT / "scenarios" / "lunar_base.yaml")
    jsonschema.validate(data, _load_schema())


def test_lunar_json_validates_against_scenario_schema():
    data = _load_scenario_dict(ROOT / "scenarios" / "lunar_base.json")
    jsonschema.validate(data, _load_schema())


def test_mars_yaml_validates_against_scenario_schema():
    data = _load_scenario_dict(ROOT / "scenarios" / "mars_habitat.yaml")
    jsonschema.validate(data, _load_schema())


def test_mars_json_validates_against_scenario_schema():
    data = _load_scenario_dict(ROOT / "scenarios" / "mars_habitat.json")
    jsonschema.validate(data, _load_schema())


def test_event_with_empty_payload_is_valid():
    data = {
        "name": "evt",
        "location": "lunar",
        "simulation": {"duration_hours": 24, "timestep_hours": 1, "crew_count": 0},
        "events": [{"time_hours": 12, "name": "unknown_future_event"}],
    }
    jsonschema.validate(data, _load_schema())


def test_unknown_event_name_is_valid():
    data = {
        "name": "evt",
        "location": "lunar",
        "simulation": {"duration_hours": 24, "timestep_hours": 1, "crew_count": 0},
        "events": [{"time_hours": 0, "name": "custom_event", "payload": {}}],
    }
    jsonschema.validate(data, _load_schema())


def test_optional_description_omitted_is_valid():
    data = {
        "name": "minimal",
        "location": "lunar",
        "simulation": {
            "duration_hours": 24,
            "timestep_hours": 1,
            "crew_count": 0,
        },
    }
    jsonschema.validate(data, _load_schema())