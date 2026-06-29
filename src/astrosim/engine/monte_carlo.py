"""Monte Carlo uncertainty analysis over simulation runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from astrosim.engine.simulator import SimulationResult, Simulator
from astrosim.engine.state import SimulationConfig


@dataclass
class MonteCarloResult:
    num_runs: int
    runs: list[SimulationResult] = field(default_factory=list)
    summary: dict[str, dict[str, float]] = field(default_factory=dict)


class MonteCarloRunner:
    """Run repeated simulations with perturbed parameters."""

    def __init__(
        self,
        base_config: SimulationConfig,
        build_simulator: Callable[[SimulationConfig], Simulator],
        seed: int | None = None,
    ) -> None:
        self.base_config = _copy_config(base_config)
        self.build_simulator = build_simulator
        self.rng = np.random.default_rng(seed)

    def run(
        self,
        num_runs: int = 100,
        perturbation: float = 0.1,
    ) -> MonteCarloResult:
        runs: list[SimulationResult] = []
        final_metrics: dict[str, list[float]] = {}

        for _ in range(num_runs):
            config = _perturb_config(self.base_config, self.rng, perturbation)
            result = self.build_simulator(config).run()
            runs.append(result)

            if result.final_state:
                for key, value in result.final_state.metrics.items():
                    final_metrics.setdefault(key, []).append(value)

        summary = {
            metric: {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "p5": float(np.percentile(values, 5)),
                "p95": float(np.percentile(values, 95)),
            }
            for metric, values in final_metrics.items()
        }

        return MonteCarloResult(num_runs=num_runs, runs=runs, summary=summary)


def _copy_config(config: SimulationConfig) -> SimulationConfig:
    return SimulationConfig(
        name=config.name,
        duration_hours=config.duration_hours,
        timestep_hours=config.timestep_hours,
        crew_count=config.crew_count,
        location=config.location,
        parameters=dict(config.parameters),
        events=list(config.events),
        subsystems=list(config.subsystems) if config.subsystems else None,
    )


def _perturb_config(
    config: SimulationConfig,
    rng: np.random.Generator,
    scale: float,
) -> SimulationConfig:
    params = dict(config.parameters)
    for key, value in params.items():
        if isinstance(value, (int, float)):
            factor = 1.0 + rng.uniform(-scale, scale)
            params[key] = type(value)(value * factor)
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