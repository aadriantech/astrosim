"""Tests for study report export."""

import json
from pathlib import Path

import jsonschema

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.export.study_report import render_study_report
from astrosim.subsystems import DEFAULT_SUBSYSTEMS

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "study_report.schema.json"


def test_render_study_report_contains_metrics(tmp_path):
    config = SimulationConfig(
        name="Report Test",
        duration_hours=12,
        timestep_hours=6,
        crew_count=2,
        parameters={"solar_array_kw": 40, "base_load_kw": 10},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
    path = render_study_report(
        result,
        output_path=tmp_path / "study_report.md",
        scenario_path="scenarios/lunar_base.yaml",
    )
    text = path.read_text()
    assert "Report Test" in text
    assert "Energy net" in text
    assert "Mass net import" in text
    assert "Mission success probability" in text
    assert "## Reproducibility" in text


def test_study_report_sidecar_validates_schema(tmp_path):
    config = SimulationConfig(
        name="Schema Test",
        duration_hours=6,
        timestep_hours=6,
        crew_count=1,
        parameters={"solar_array_kw": 20, "base_load_kw": 5},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
    render_study_report(result, output_path=tmp_path / "study_report.md")
    sidecar = json.loads((tmp_path / "study_report.json").read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(sidecar, schema)