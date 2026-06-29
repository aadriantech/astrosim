#!/usr/bin/env python3
"""Greenhouse lunar scenario with export and dashboard."""

from pathlib import Path

from astrosim.export.formats import export_json
from astrosim.scenario import load_and_build
from astrosim.visualization.dashboard import plot_dashboard

ROOT = Path(__file__).resolve().parent.parent
SCENARIO = ROOT / "scenarios" / "greenhouse_lunar.yaml"
OUTPUT = ROOT / "output" / "greenhouse_lunar"


def main() -> None:
    result = load_and_build(SCENARIO).run()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_json(result, OUTPUT / "greenhouse_lunar.json")
    plot_dashboard(result, OUTPUT / "greenhouse_lunar_dashboard.png")
    final = result.final_state
    assert final is not None
    print(f"Scenario: {result.config.name}")
    print(f"Food net import: {final.metrics.get('eclss.food_net_import_kg', 0):.2f} kg")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()