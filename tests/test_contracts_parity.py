"""Contract tests: lunar_base.json parameters match lunar_base.yaml."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _load_parameters(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = yaml.safe_load(text)
    return data.get("parameters", {})


def test_lunar_json_parameter_keys_match_yaml():
    yaml_params = _load_parameters(ROOT / "scenarios" / "lunar_base.yaml")
    json_params = _load_parameters(ROOT / "scenarios" / "lunar_base.json")
    assert set(json_params) == set(yaml_params)


def test_lunar_json_parameter_values_match_yaml():
    yaml_params = _load_parameters(ROOT / "scenarios" / "lunar_base.yaml")
    json_params = _load_parameters(ROOT / "scenarios" / "lunar_base.json")
    for key, value in yaml_params.items():
        assert json_params[key] == value, f"parameter {key!r} differs"