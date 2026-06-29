"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from astrosim.ai.hooks import AIHooks, InsightRequest
from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.export.formats import export_csv, export_json
from astrosim.scenario import build_simulator, load_and_build, load_scenario
from astrosim.visualization.dashboard import plot_dashboard
from astrosim.visualization.web import render_web_dashboard


def main() -> None:
    parser = argparse.ArgumentParser(description="AstroSim habitat simulator")
    parser.add_argument(
        "scenario",
        type=Path,
        help="Path to scenario YAML or JSON file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory for results",
    )
    parser.add_argument("--no-plot", action="store_true", help="Skip matplotlib dashboard")
    parser.add_argument("--web", action="store_true", help="Generate HTML web dashboard")
    parser.add_argument(
        "--monte-carlo",
        type=int,
        metavar="N",
        help="Run N Monte Carlo perturbation runs and write summary JSON",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for Monte Carlo runs",
    )
    args = parser.parse_args()

    config = load_scenario(args.scenario)
    simulator = load_and_build(args.scenario)
    result = simulator.run()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    name = result.config.name.replace(" ", "_").lower()

    export_json(result, out / f"{name}.json")
    export_csv(result, out / f"{name}.csv")
    if not args.no_plot:
        plot_dashboard(result, out / f"{name}_dashboard.png")
    if args.web:
        render_web_dashboard(result, out / f"{name}_dashboard.html")

    hooks = AIHooks()
    insights = hooks.generate_insights(InsightRequest(result=result))
    print(insights)

    suggestions = hooks.suggest_optimizations(result)
    if suggestions:
        print("\nOptimization suggestions:")
        for suggestion in suggestions:
            print(
                f"  {suggestion.parameter}: "
                f"{suggestion.current_value} -> {suggestion.suggested_value} "
                f"({suggestion.rationale})"
            )

    if args.monte_carlo:
        mc_result = MonteCarloRunner(
            base_config=config,
            build_simulator=build_simulator,
            seed=args.seed,
        ).run(num_runs=args.monte_carlo)
        mc_path = out / f"{name}_monte_carlo_summary.json"
        mc_path.write_text(json.dumps(mc_result.summary, indent=2))
        print(f"\nMonte Carlo: {mc_result.num_runs} runs written to {mc_path.name}")

    print(f"\nResults written to {out.resolve()}")


if __name__ == "__main__":
    main()