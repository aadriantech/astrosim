"""Contract tests: optimization_result.schema.json."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import jsonschema
import pytest

from astrosim.analysis.optimize import minimize_metric
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "optimization_result.schema.json"

pytest.importorskip("scipy")


def test_optimization_result_validates_against_schema():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 72
    config.timestep_hours = 12

    result = minimize_metric(
        config,
        build_simulator,
        parameter="solar_array_kw",
        metric_key="energy.net_kwh",
        bounds=(50.0, 120.0),
    )

    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(asdict(result), schema)