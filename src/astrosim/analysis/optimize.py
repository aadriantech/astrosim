"""Parameter optimization over simulation metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from astrosim.analysis.sensitivity import _extract_metric, _with_parameter
from astrosim.engine.simulator import Simulator
from astrosim.engine.state import SimulationConfig


@dataclass
class OptimizationResult:
    parameter: str
    metric: str
    optimal_value: float
    metric_value: float
    success: bool
    iterations: int
    message: str


def minimize_metric(
    base_config: SimulationConfig,
    build_simulator: Callable[[SimulationConfig], Simulator],
    *,
    parameter: str,
    metric_key: str,
    bounds: tuple[float, float],
    method: str = "bounded",
) -> OptimizationResult:
    """Find parameter value in bounds that minimizes the target metric."""
    baseline = base_config.parameters.get(parameter)
    if not isinstance(baseline, (int, float)):
        raise TypeError(f"Parameter '{parameter}' must be numeric")

    try:
        from scipy import optimize as scipy_optimize
    except ImportError as exc:
        raise ImportError(
            "scipy is required for optimization. Install with: pip install astrosim[optimize]"
        ) from exc

    iterations = 0

    def objective(value: float) -> float:
        nonlocal iterations
        iterations += 1
        config = _with_parameter(base_config, parameter, value)
        result = build_simulator(config).run()
        return _extract_metric(result, metric_key)

    opt = scipy_optimize.minimize_scalar(
        objective,
        bounds=bounds,
        method=method,
    )

    optimal_value = float(opt.x)
    config = _with_parameter(base_config, parameter, optimal_value)
    metric_value = _extract_metric(build_simulator(config).run(), metric_key)

    return OptimizationResult(
        parameter=parameter,
        metric=metric_key,
        optimal_value=optimal_value,
        metric_value=metric_value,
        success=bool(opt.success),
        iterations=iterations + 1,
        message=str(opt.message),
    )