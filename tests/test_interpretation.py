"""Tests for result interpretation and study report verdict sections."""

import json
from pathlib import Path

from astrosim.export.interpretation import interpret_result
from astrosim.export.study_report import render_study_report
from astrosim.scenario import load_and_build

ROOT = Path(__file__).resolve().parent.parent


def test_interpret_energy_deficit_lunar():
    result = load_and_build(ROOT / "scenarios" / "lunar_base.yaml").run()
    interp = interpret_result(result)
    assert interp.energy_status in ("critical_deficit", "marginal_deficit")
    assert interp.verdict
    assert any("Energy" in s for s in interp.implications)


def test_interpret_greenhouse_food_credit():
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    interp = interpret_result(result)
    assert any("Greenhouse" in s or "food" in s.lower() for s in interp.implications)


def test_study_report_includes_verdict(tmp_path):
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    path = render_study_report(result, output_path=tmp_path / "study_report.md")
    text = path.read_text()
    assert "## Implications" in text
    assert "## Verdict" in text
    sidecar = json.loads((tmp_path / "study_report.json").read_text())
    assert "verdict" in sidecar
    assert "implications" in sidecar
    assert len(sidecar["implications"]) >= 1