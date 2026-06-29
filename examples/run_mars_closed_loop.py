#!/usr/bin/env python3
"""Mars closed-loop habitat demo with export."""

from pathlib import Path

from astrosim.export.formats import export_json
from astrosim.scenario import load_and_build

ROOT = Path(__file__).resolve().parent.parent
SCENARIO = ROOT / "scenarios" / "mars_closed_loop.yaml"
OUTPUT = ROOT / "output" / "mars_closed_loop"


def main() -> None:
    result = load_and_build(SCENARIO).run()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_json(result, OUTPUT / "mars_closed_loop.json")
    final = result.final_state
    assert final is not None
    print(f"Scenario: {result.config.name}")
    print(f"Food net import: {final.metrics.get('eclss.food_net_import_kg', 0):.2f} kg")
    print(f"Water net: {final.metrics.get('eclss.water_net_kg', 0):.2f} kg")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()