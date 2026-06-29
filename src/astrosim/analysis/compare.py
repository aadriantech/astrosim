"""Multi-scenario comparison utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean, pstdev

import pandas as pd

from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.engine.simulator import SimulationResult
from astrosim.scenario import build_simulator, load_and_build, load_scenario


def _resolve_metric(sim_result: SimulationResult, metric: str) -> float | None:
    final = sim_result.final_state
    if final is not None and metric in final.metrics:
        return final.metrics[metric]
    if metric == "energy.net_kwh" and sim_result.energy_budget:
        return sim_result.energy_budget.net_kwh
    if metric == "mass.net_import_kg" and sim_result.mass_budget:
        return sim_result.mass_budget.net_import_kg
    if metric in ("reliability.success", "reliability.mission_success_probability"):
        if sim_result.reliability_budget:
            return sim_result.reliability_budget.mission_success_probability
    return None


@dataclass
class CompareResult:
    metrics: list[str]
    rows: list[dict[str, str | float | None]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _mc_metric_stats(
    config,
    metric: str,
    *,
    monte_carlo_runs: int,
    seed: int | None,
) -> tuple[float | None, float | None]:
    config.duration_hours = min(config.duration_hours, 48)
    mc = MonteCarloRunner(config, build_simulator, seed=seed).run(num_runs=monte_carlo_runs)
    values = [_resolve_metric(run, metric) for run in mc.runs]
    values = [v for v in values if v is not None]
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], 0.0
    return mean(values), pstdev(values)


def compare_scenarios(
    paths: list[str | Path],
    metrics: list[str],
    *,
    monte_carlo_runs: int | None = None,
    seed: int | None = None,
) -> CompareResult:
    """Run scenarios and collect final-step metric values."""
    columns = list(metrics)
    if monte_carlo_runs:
        for metric in metrics:
            columns.extend([f"{metric}_mean", f"{metric}_std"])
    result = CompareResult(metrics=columns)
    for path in paths:
        scenario_path = Path(path)
        try:
            config = load_scenario(scenario_path)
            sim_result = load_and_build(scenario_path).run()
            row: dict[str, str | float | None] = {"scenario_name": config.name}
            for metric in metrics:
                row[metric] = _resolve_metric(sim_result, metric)
                if monte_carlo_runs:
                    m, s = _mc_metric_stats(
                        load_scenario(scenario_path),
                        metric,
                        monte_carlo_runs=monte_carlo_runs,
                        seed=seed,
                    )
                    row[f"{metric}_mean"] = m
                    row[f"{metric}_std"] = s
            result.rows.append(row)
        except Exception as exc:  # noqa: BLE001 — collect per-scenario errors
            result.errors.append(f"{scenario_path}: {exc}")
    return result


def export_compare_csv(result: CompareResult, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    columns = ["scenario_name", *result.metrics]
    frame = pd.DataFrame(result.rows, columns=columns)
    frame.to_csv(output, index=False)
    return output


def format_compare_table(result: CompareResult) -> str:
    if not result.rows:
        return "No scenario results."
    columns = ["scenario_name", *result.metrics]
    lines = ["\t".join(columns)]
    for row in result.rows:
        cells = [str(row.get(col, "")) for col in columns]
        lines.append("\t".join(cells))
    return "\n".join(lines)