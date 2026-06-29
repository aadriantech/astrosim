"""Tests for parameter optimization."""

from __future__ import annotations

import pytest

from astrosim.analysis.optimize import minimize_metric
from astrosim.engine.state import SimulationConfig
from astrosim.scenario import build_simulator, load_scenario
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


pytest.importorskip("scipy")


def test_minimize_metric_improves_energy_net():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 168
    config.timestep_hours = 12

    result = minimize_metric(
        config,
        build_simulator,
        parameter="solar_array_kw",
        metric_key="energy.net_kwh",
        bounds=(40.0, 200.0),
    )

    assert result.parameter == "solar_array_kw"
    assert result.metric == "energy.net_kwh"
    assert 40.0 <= result.optimal_value <= 200.0
    assert result.iterations >= 1


def test_minimize_metric_requires_numeric_parameter():
    config = SimulationConfig(
        name="t",
        duration_hours=24,
        timestep_hours=12,
        parameters={"label": "not-a-number"},
    )
    with pytest.raises(TypeError):
        minimize_metric(
            config,
            build_simulator,
            parameter="label",
            metric_key="energy.net_kwh",
            bounds=(1.0, 2.0),
        )