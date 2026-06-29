#!/usr/bin/env python3
"""Compare lunar, Mars, and orbital scenarios."""

from pathlib import Path

from astrosim.analysis.compare import compare_scenarios, export_compare_csv, format_compare_table

ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = [
    ROOT / "scenarios" / "lunar_base.yaml",
    ROOT / "scenarios" / "mars_habitat.yaml",
    ROOT / "scenarios" / "orbital_station.yaml",
]
METRICS = ["energy.net_kwh", "eclss.water_net_kg", "reliability.success"]
OUTPUT = ROOT / "output" / "compare"


def main() -> None:
    result = compare_scenarios(SCENARIOS, METRICS)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_compare_csv(result, OUTPUT / "scenario_compare.csv")
    print(format_compare_table(result))
    if result.errors:
        for err in result.errors:
            print(f"WARN: {err}")
    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()