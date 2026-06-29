#!/usr/bin/env python3
"""Run Pareto trade study for lunar base solar vs battery."""

from pathlib import Path

from astrosim.analysis.pareto import export_trade_study_csv, run_trade_study
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "trade_study"


def main() -> None:
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    config.duration_hours = 168
    config.timestep_hours = 12

    result = run_trade_study(
        config,
        build_simulator,
        param_x="solar_array_kw",
        param_y="battery_kwh",
        values_x=[60.0, 80.0, 100.0, 120.0, 140.0],
        values_y=[200.0, 400.0, 600.0, 800.0],
        metric_a="energy.net_kwh",
        metric_b="reliability.success",
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = export_trade_study_csv(result, OUTPUT / "lunar_solar_battery.csv")
    print(f"Points: {len(result.points)}")
    print(f"Pareto-optimal: {len(result.pareto_points)}")
    print(f"Output: {path.resolve()}")


if __name__ == "__main__":
    main()