#!/usr/bin/env python3
"""Run the lunar base example scenario."""

from pathlib import Path

from astrosim.ai.hooks import AIHooks, InsightRequest
from astrosim.export.formats import export_csv, export_json
from astrosim.scenario import load_and_build
from astrosim.visualization.dashboard import plot_dashboard
from astrosim.visualization.web import render_web_dashboard

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "lunar_base"


def main() -> None:
    simulator = load_and_build(ROOT / "scenarios" / "lunar_base.yaml")
    result = simulator.run()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_json(result, OUTPUT / "results.json")
    export_csv(result, OUTPUT / "results.csv")
    plot_dashboard(result, OUTPUT / "dashboard.png")
    render_web_dashboard(result, OUTPUT / "dashboard.html")

    ai = AIHooks()
    print(ai.generate_insights(InsightRequest(result=result)))
    for suggestion in ai.suggest_optimizations(result):
        print(f"  → {suggestion.parameter}: {suggestion.rationale}")

    print(f"\nOutput: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()