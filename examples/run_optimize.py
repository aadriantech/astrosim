#!/usr/bin/env python3
"""Run parameter optimization for lunar base energy balance."""

from pathlib import Path

from astrosim.analysis.optimize import minimize_metric
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    short = config
    short.duration_hours = 168
    short.timestep_hours = 12

    result = minimize_metric(
        short,
        build_simulator,
        parameter="solar_array_kw",
        metric_key="energy.net_kwh",
        bounds=(40.0, 160.0),
    )

    print(f"Optimize: {result.parameter} → {result.metric}")
    print(f"Optimal {result.parameter}={result.optimal_value:.2f}")
    print(f"Metric value={result.metric_value:.2f}")
    print(f"Success={result.success} iterations={result.iterations}")


if __name__ == "__main__":
    main()