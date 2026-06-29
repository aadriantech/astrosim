#!/usr/bin/env python3
"""Run the orbital station example scenario."""

from pathlib import Path

from astrosim.export.formats import export_csv, export_json
from astrosim.scenario import load_and_build

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "orbital_station"


def main() -> None:
    simulator = load_and_build(ROOT / "scenarios" / "orbital_station.yaml")
    result = simulator.run()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_json(result, OUTPUT / "results.json")
    export_csv(result, OUTPUT / "results.csv")

    print(f"Scenario: {result.config.name}")
    print(f"Steps: {len(result.history)}")
    print(f"Energy net: {result.energy_budget.net_kwh:.1f} kWh")
    print(f"Output: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()