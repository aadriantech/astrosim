"""Contract tests for validation_report.schema.json."""

import json
from pathlib import Path

import jsonschema

from astrosim.scenario import load_and_build
from astrosim.validation.validate import validate_result

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "contracts" / "validation_report.schema.json"


def test_validation_report_matches_schema():
    result = load_and_build(ROOT / "scenarios" / "orbital_station.yaml").run()
    report = validate_result(result, scenario_path="scenarios/orbital_station.yaml")
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