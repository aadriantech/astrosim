"""Sensitivity analysis over simulation parameters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from astrosim.engine.simulator import SimulationResult, Simulator
from astrosim.engine.state import SimulationConfig


@dataclass
class SensitivityResult:
    parameter: str
    baseline_value: float
    metric: str
    perturbations: list[float] = field(default_factory=list)
    metric_values: list[float] = field(default_factory=list)
    elasticity: float = 0.0


def one_at_a_time_sensitivity(
    base_config: SimulationConfig,
    build_simulator: Callable[[SimulationConfig], Simulator],
    parameter: str,
    metric_key: str,
    perturbation_range: tuple[float, float] = (-0.2, 0.2),
    num_points: int = 11,
) -> SensitivityResult:
    """Vary one parameter and measure metric response."""
    baseline = base_config.parameters.get(parameter)
    if not isinstance(baseline, (int, float)):
        raise ValueError(f"Parameter '{parameter}' must be numeric")

    factors = np.linspace(1 + perturbation_range[0], 1 + perturbation_range[1], num_points)
    values: list[float] = []
    metrics: list[float] = []

    for factor in factors:
        value = float(baseline) * factor
        config = _with_parameter(base_config, parameter, value)
        result = build_simulator(config).run()
        metric = _extract_metric(result, metric_key)
        values.append(value)
        metrics.append(metric)

    elasticity = _compute_elasticity(values, metrics, float(baseline))

    return SensitivityResult(
        parameter=parameter,
        baseline_value=float(baseline),
        metric=metric_key,
        perturbations=values,
        metric_values=metrics,
        elasticity=elasticity,
    )


def _with_parameter(
    config: SimulationConfig, key: str, value: float
) -> SimulationConfig:
    params = dict(config.parameters)
    params[key] = value
    return SimulationConfig(
        name=config.name,
        duration_hours=config.duration_hours,
        timestep_hours=config.timestep_hours,
        crew_count=config.crew_count,
        location=config.location,
        parameters=params,
        events=config.events,
        subsystems=config.subsystems,
    )


def _extract_metric(result: SimulationResult, metric_key: str) -> float:
    if result.energy_budget and metric_key == "energy.net_kwh":
        return result.energy_budget.net_kwh
    if result.mass_budget and metric_key == "mass.net_import_kg":
        return result.mass_budget.net_import_kg
    if result.reliability_budget and metric_key == "reliability.success":
        return result.reliability_budget.mission_success_probability
    if result.final_state and metric_key in result.final_state.metrics:
        return result.final_state.metrics[metric_key]
    raise KeyError(f"Unknown metric '{metric_key}'")


def _compute_elasticity(
    values: list[float], metrics: list[float], baseline: float
) -> float:
    if len(values) < 2 or baseline == 0:
        return 0.0
    d_metric = metrics[-1] - metrics[0]
    d_value = values[-1] - values[0]
    mid_metric = np.mean(metrics)
    if mid_metric == 0 or d_value == 0:
        return 0.0
    return (d_metric / mid_metric) / (d_value / baseline)