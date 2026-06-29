#!/usr/bin/env python3
"""Run canonical scenario suite and export JSON report."""

from pathlib import Path

from astrosim.analysis.suite import export_suite_json, run_scenario_suite

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "suite"


def main() -> None:
    result = run_scenario_suite(ROOT / "scenarios")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = export_suite_json(result, OUTPUT / "suite_report.json")
    ok = sum(1 for row in result.rows if row.error is None)
    print(f"Suite: {ok}/{len(result.rows)} scenarios OK")
    print(f"Written to {path}")


if __name__ == "__main__":
    main()