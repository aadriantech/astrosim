"""Tests for Pareto trade study."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import jsonschema
import pytest

from astrosim.analysis.pareto import export_trade_study_csv, run_trade_study
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent


def test_trade_study_finds_pareto_points():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 72
    config.timestep_hours = 12

    result = run_trade_study(
        config,
        build_simulator,
        param_x="solar_array_kw",
        param_y="battery_kwh",
        values_x=[60.0, 80.0, 100.0, 120.0],
        values_y=[200.0, 400.0, 600.0],
        metric_a="energy.net_kwh",
        metric_b="reliability.success",
        maximize_a=True,
        maximize_b=True,
    )

    assert len(result.points) == 12
    assert len(result.pareto_points) >= 1


def test_export_trade_study_csv(tmp_path):
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 48
    config.timestep_hours = 12

    result = run_trade_study(
        config,
        build_simulator,
        param_x="solar_array_kw",
        param_y="battery_kwh",
        values_x=[70.0, 90.0],
        values_y=[300.0, 500.0],
        metric_a="energy.net_kwh",
        metric_b="reliability.success",
    )
    path = export_trade_study_csv(result, tmp_path / "trade.csv")
    text = path.read_text()
    assert "solar_array_kw" in text
    assert "pareto_optimal" in text


def test_trade_study_with_monte_carlo_envelope():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 48
    config.timestep_hours = 12

    result = run_trade_study(
        config,
        build_simulator,
        param_x="solar_array_kw",
        param_y="battery_kwh",
        values_x=[80.0, 100.0],
        values_y=[400.0],
        metric_a="energy.net_kwh",
        metric_b="reliability.success",
        monte_carlo_runs=3,
        mc_seed=1,
    )

    assert len(result.points) == 2
    assert result.points[0].metric_a_std >= 0.0


def test_trade_study_schema():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 48
    config.timestep_hours = 12
    result = run_trade_study(
        config,
        build_simulator,
        param_x="solar_array_kw",
        param_y="battery_kwh",
        values_x=[80.0],
        values_y=[400.0],
        metric_a="energy.net_kwh",
        metric_b="reliability.success",
    )
    payload = {
        "param_x": result.param_x,
        "param_y": result.param_y,
        "metric_a": result.metric_a,
        "metric_b": result.metric_b,
        "points": [asdict(p) for p in result.points],
    }
    schema = json.loads(
        (ROOT / "contracts" / "trade_study.schema.json").read_text()
    )
    jsonschema.validate(payload, schema)