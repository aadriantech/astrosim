"""Two-parameter trade study and Pareto frontier extraction."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from astrosim.analysis.sensitivity import _extract_metric, _with_parameter
from astrosim.engine.simulator import Simulator
from astrosim.engine.state import SimulationConfig


@dataclass
class TradeStudyPoint:
    param_x: float
    param_y: float
    metric_a: float
    metric_b: float
    pareto_optimal: bool = False


@dataclass
class TradeStudyResult:
    param_x: str
    param_y: str
    metric_a: str
    metric_b: str
    points: list[TradeStudyPoint] = field(default_factory=list)

    @property
    def pareto_points(self) -> list[TradeStudyPoint]:
        return [p for p in self.points if p.pareto_optimal]


def run_trade_study(
    base_config: SimulationConfig,
    build_simulator: Callable[[SimulationConfig], Simulator],
    *,
    param_x: str,
    param_y: str,
    values_x: list[float],
    values_y: list[float],
    metric_a: str,
    metric_b: str,
    maximize_a: bool = True,
    maximize_b: bool = True,
) -> TradeStudyResult:
    """Grid sweep two parameters; mark Pareto-optimal points on two metrics."""
    points: list[TradeStudyPoint] = []

    for x in values_x:
        for y in values_y:
            config = _with_parameter(base_config, param_x, x)
            config = _with_parameter(config, param_y, y)
            result = build_simulator(config).run()
            points.append(
                TradeStudyPoint(
                    param_x=x,
                    param_y=y,
                    metric_a=_extract_metric(result, metric_a),
                    metric_b=_extract_metric(result, metric_b),
                )
            )

    _mark_pareto(points, maximize_a=maximize_a, maximize_b=maximize_b)

    return TradeStudyResult(
        param_x=param_x,
        param_y=param_y,
        metric_a=metric_a,
        metric_b=metric_b,
        points=points,
    )


def export_trade_study_csv(result: TradeStudyResult, path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                result.param_x,
                result.param_y,
                result.metric_a,
                result.metric_b,
                "pareto_optimal",
            ],
        )
        writer.writeheader()
        for point in result.points:
            writer.writerow(
                {
                    result.param_x: point.param_x,
                    result.param_y: point.param_y,
                    result.metric_a: point.metric_a,
                    result.metric_b: point.metric_b,
                    "pareto_optimal": point.pareto_optimal,
                }
            )
    return output


def _mark_pareto(
    points: list[TradeStudyPoint],
    *,
    maximize_a: bool,
    maximize_b: bool,
) -> None:
    for i, candidate in enumerate(points):
        dominated = False
        for j, other in enumerate(points):
            if i == j:
                continue
            if _dominates(
                other.metric_a,
                other.metric_b,
                candidate.metric_a,
                candidate.metric_b,
                maximize_a=maximize_a,
                maximize_b=maximize_b,
            ):
                dominated = True
                break
        candidate.pareto_optimal = not dominated


def _dominates(
    a1: float,
    b1: float,
    a2: float,
    b2: float,
    *,
    maximize_a: bool,
    maximize_b: bool,
) -> bool:
    better_a = a1 >= a2 if maximize_a else a1 <= a2
    better_b = b1 >= b2 if maximize_b else b1 <= b2
    strictly_a = a1 > a2 if maximize_a else a1 < a2
    strictly_b = b1 > b2 if maximize_b else b1 < b2
    return better_a and better_b and (strictly_a or strictly_b)