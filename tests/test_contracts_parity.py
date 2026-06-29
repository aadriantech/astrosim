"""Contract tests: JSON/YAML scenario parity for canonical missions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent

SCENARIO_PAIRS = [
    ("lunar_base", ROOT / "scenarios" / "lunar_base.yaml", ROOT / "scenarios" / "lunar_base.json"),
    ("mars_habitat", ROOT / "scenarios" / "mars_habitat.yaml", ROOT / "scenarios" / "mars_habitat.json"),
    (
        "orbital_station",
        ROOT / "scenarios" / "orbital_station.yaml",
        ROOT / "scenarios" / "orbital_station.json",
    ),
    (
        "deep_space_transit",
        ROOT / "scenarios" / "deep_space_transit.yaml",
        ROOT / "scenarios" / "deep_space_transit.json",
    ),
    (
        "greenhouse_lunar",
        ROOT / "scenarios" / "greenhouse_lunar.yaml",
        ROOT / "scenarios" / "greenhouse_lunar.json",
    ),
]


def _load_scenario_dict(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _parity_view(data: dict) -> dict:
    """Comparable subset: structural fields consumed by config_from_dict."""
    return {
        "name": data["name"],
        "location": data["location"],
        "simulation": data["simulation"],
        "events": data.get("events", []),
        "parameters": data.get("parameters", {}),
    }


def _load_parameters(path: Path) -> dict:
    return _load_scenario_dict(path).get("parameters", {})


@pytest.mark.parametrize("stem,yaml_path,json_path", SCENARIO_PAIRS)
def test_json_parameter_keys_match_yaml(stem, yaml_path, json_path):
    yaml_params = _load_parameters(yaml_path)
    json_params = _load_parameters(json_path)
    assert set(json_params) == set(yaml_params), stem


@pytest.mark.parametrize("stem,yaml_path,json_path", SCENARIO_PAIRS)
def test_json_parameter_values_match_yaml(stem, yaml_path, json_path):
    yaml_params = _load_parameters(yaml_path)
    json_params = _load_parameters(json_path)
    for key, value in yaml_params.items():
        assert json_params[key] == value, f"{stem}: parameter {key!r} differs"


@pytest.mark.parametrize("stem,yaml_path,json_path", SCENARIO_PAIRS)
def test_json_structural_parity_with_yaml(stem, yaml_path, json_path):
    yaml_view = _parity_view(_load_scenario_dict(yaml_path))
    json_view = _parity_view(_load_scenario_dict(json_path))
    assert yaml_view == json_view, stem