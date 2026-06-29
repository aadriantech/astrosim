#!/usr/bin/env python3
"""Run deep space transit example."""

from pathlib import Path

from astrosim.export.formats import export_json
from astrosim.scenario import load_and_build

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "deep_space_transit"


def main() -> None:
    result = load_and_build(ROOT / "scenarios" / "deep_space_transit.yaml").run()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_json(result, OUTPUT / "results.json")
    print(f"Steps: {len(result.history)}")
    print(f"Energy net: {result.energy_budget.net_kwh:.1f} kWh")
    print(f"Output: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()