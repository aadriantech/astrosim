"""Tests for scenario suite runner."""

import json
from pathlib import Path

import jsonschema

from astrosim.analysis.suite import export_suite_json, run_scenario_suite

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "suite_report.schema.json"


def test_run_scenario_suite_covers_canonical():
    result = run_scenario_suite(ROOT / "scenarios")
    assert len(result.rows) >= 5
    assert all(row.scenario_name for row in result.rows)
    assert not result.errors


def test_suite_export_validates_schema(tmp_path):
    result = run_scenario_suite(ROOT / "scenarios", names=("lunar_base.yaml",))
    path = export_suite_json(result, tmp_path / "suite.json")
    payload = json.loads(path.read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)