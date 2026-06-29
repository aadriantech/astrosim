#!/usr/bin/env python3
"""Run one-at-a-time sensitivity analysis for a scenario parameter."""

from pathlib import Path

from astrosim.analysis.sensitivity import one_at_a_time_sensitivity
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    result = one_at_a_time_sensitivity(
        config,
        build_simulator,
        parameter="solar_array_kw",
        metric_key="energy.net_kwh",
        num_points=7,
    )

    print(f"Sensitivity: {result.parameter} → {result.metric}")
    print(f"Baseline: {result.baseline_value}")
    print(f"Elasticity: {result.elasticity:.4f}")
    print()
    for value, metric in zip(result.perturbations, result.metric_values):
        print(f"  {result.parameter}={value:8.2f}  {result.metric}={metric:10.2f}")


if __name__ == "__main__":
    main()