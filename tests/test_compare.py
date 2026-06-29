"""Tests for scenario comparison API."""

import json
from pathlib import Path

import jsonschema

from astrosim.analysis.compare import compare_scenarios, export_compare_csv, format_compare_table

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "scenario_compare.schema.json"


def test_compare_scenarios_returns_rows():
    paths = [
        ROOT / "scenarios" / "lunar_base.yaml",
        ROOT / "scenarios" / "mars_habitat.yaml",
    ]
    result = compare_scenarios(paths, ["power.stored_kwh", "eclss.water_net_kg"])
    assert len(result.rows) == 2
    assert result.rows[0]["scenario_name"]
    assert "power.stored_kwh" in result.rows[0]


def test_export_compare_csv(tmp_path):
    paths = [ROOT / "scenarios" / "orbital_station.yaml"]
    result = compare_scenarios(paths, ["thermal.delta_t_c"])
    path = export_compare_csv(result, tmp_path / "compare.csv")
    assert path.exists()
    assert "scenario_name" in path.read_text()


def test_compare_schema_validation():
    paths = [ROOT / "scenarios" / "lunar_base.yaml"]
    result = compare_scenarios(paths, ["eclss.co2_ppm"])
    payload = {
        "metrics": result.metrics,
        "rows": result.rows,
        "errors": result.errors,
    }
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)


def test_format_compare_table():
    paths = [ROOT / "scenarios" / "lunar_base.yaml"]
    result = compare_scenarios(paths, ["eclss.co2_ppm"])
    table = format_compare_table(result)
    assert "scenario_name" in table
    assert "Lunar" in table


def test_compare_resolves_budget_metrics():
    paths = [ROOT / "scenarios" / "lunar_base.yaml"]
    result = compare_scenarios(paths, ["energy.net_kwh", "mass.net_import_kg"])
    assert result.rows[0]["energy.net_kwh"] is not None
    assert result.rows[0]["mass.net_import_kg"] is not None


def test_compare_monte_carlo_adds_mean_std():
    paths = [ROOT / "scenarios" / "greenhouse_lunar.yaml"]
    result = compare_scenarios(
        paths,
        ["reliability.success"],
        monte_carlo_runs=3,
        seed=1,
    )
    row = result.rows[0]
    assert "reliability.success_mean" in row
    assert "reliability.success_std" in row
    assert row["reliability.success_mean"] is not None