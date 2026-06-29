"""Interpretation v2: references and structured actions."""

import json
from pathlib import Path

from astrosim.export.interpretation import interpret_result
from astrosim.export.study_report import render_study_report
from astrosim.scenario import load_and_build

ROOT = Path(__file__).resolve().parent.parent


def test_interpret_result_includes_references():
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    interp = interpret_result(result)
    assert interp.references
    assert any("BVAD" in ref or "OCHMO" in ref for ref in interp.references)


def test_interpret_result_includes_actions_on_deficit():
    result = load_and_build(ROOT / "scenarios" / "lunar_base.yaml").run()
    interp = interpret_result(result)
    assert interp.actions
    params = {a.parameter for a in interp.actions}
    assert "solar_array_kw" in params


def test_study_report_includes_references_and_actions(tmp_path):
    result = load_and_build(ROOT / "scenarios" / "lunar_base.yaml").run()
    path = render_study_report(
        result,
        output_path=tmp_path / "study_report.md",
        scenario_path="scenarios/lunar_base.yaml",
    )
    text = path.read_text()
    assert "## References" in text
    assert "## Recommended Actions" in text
    sidecar = json.loads((tmp_path / "study_report.json").read_text())
    assert "references" in sidecar
    assert "actions" in sidecar
    assert len(sidecar["actions"]) >= 1


def test_study_report_includes_validation_when_provided(tmp_path):
    from astrosim.validation.validate import validate_result

    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    validation = validate_result(result)
    path = render_study_report(
        result,
        output_path=tmp_path / "study_report.md",
        scenario_path="scenarios/greenhouse_lunar.yaml",
        validation=validation,
    )
    text = path.read_text()
    assert "## Validation" in text
    sidecar = json.loads((tmp_path / "study_report.json").read_text())
    assert "validation" in sidecar
    assert sidecar["validation"]["overall_status"] in ("pass", "warn", "fail")