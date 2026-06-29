"""Reference validation against official benchmarks."""

import json
from pathlib import Path

import jsonschema
import pytest

from astrosim.scenario import load_and_build
from astrosim.validation.benchmarks import default_benchmarks_path, load_benchmarks
from astrosim.validation.validate import (
    format_validation_table,
    validate_result,
)

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "validation_report.schema.json"


def test_benchmarks_file_exists():
    path = default_benchmarks_path()
    assert path.exists()
    data = load_benchmarks(path)
    assert "eclss_consumables" in data
    assert data["eclss_consumables"]["parameters"]["o2_kg_per_person_day"]["value"] == 0.84


def test_parameter_fidelity_o2_passes():
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    report = validate_result(result)
    o2_checks = [c for c in report.checks if c.name == "o2_kg_per_person_day"]
    assert o2_checks
    assert o2_checks[0].status == "pass"
    assert o2_checks[0].category == "parameter_fidelity"


def test_derived_o2_rate_matches_parameter():
    result = load_and_build(ROOT / "scenarios" / "orbital_station.yaml").run()
    report = validate_result(result)
    derived = [c for c in report.checks if c.name == "derived_o2_kg_per_person_day"]
    assert derived
    assert derived[0].status == "pass"
    assert derived[0].simulated == pytest.approx(0.84, rel=0.01)


def test_orbital_station_envelope_mass_import_passes():
    result = load_and_build(ROOT / "scenarios" / "orbital_station.yaml").run()
    report = validate_result(result)
    mass = [c for c in report.checks if c.name == "mass_net_import_kg_per_crew_year"]
    assert mass
    assert mass[0].status == "pass"


def test_validation_report_overall_not_fail_for_canonical_scenarios():
    for scenario in ("greenhouse_lunar.yaml", "orbital_station.yaml", "lunar_base.yaml"):
        result = load_and_build(ROOT / "scenarios" / scenario).run()
        report = validate_result(result)
        assert report.overall_status in ("pass", "warn"), (
            f"{scenario}: {report.overall_status} — "
            + "; ".join(c.message for c in report.checks if c.status == "fail")
        )


def test_validation_report_schema(tmp_path):
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    report = validate_result(result)
    payload = {
        "scenario_name": report.scenario_name,
        "overall_status": report.overall_status,
        "checks": [
            {
                "name": c.name,
                "category": c.category,
                "simulated": c.simulated,
                "reference": c.reference,
                "status": c.status,
                "message": c.message,
                "source": c.source,
            }
            for c in report.checks
        ],
    }
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)


def test_format_validation_table_includes_status():
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    report = validate_result(result)
    table = format_validation_table(report)
    assert "PASS" in table or "WARN" in table
    assert "o2_kg_per_person_day" in table