#!/usr/bin/env python3
"""Run the Mars habitat example scenario with Monte Carlo analysis."""

from pathlib import Path

from astrosim.ai.hooks import AIHooks, InsightRequest
from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.export.formats import export_json
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "mars_habitat"


def main() -> None:
    config = load_scenario(ROOT / "scenarios" / "mars_habitat.yaml")
    result = build_simulator(config).run()

    mc = MonteCarloRunner(
        base_config=config,
        build_simulator=build_simulator,
        seed=42,
    )
    mc_result = mc.run(num_runs=50, perturbation=0.08)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    export_json(result, OUTPUT / "results.json")

    summary_path = OUTPUT / "monte_carlo_summary.json"
    import json

    summary_path.write_text(json.dumps(mc_result.summary, indent=2))

    print(AIHooks().generate_insights(InsightRequest(result=result)))
    print(f"\nMonte Carlo runs: {mc_result.num_runs}")
    for metric, stats in list(mc_result.summary.items())[:5]:
        print(f"  {metric}: mean={stats['mean']:.4f}, std={stats['std']:.4f}")
    print(f"\nOutput: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()