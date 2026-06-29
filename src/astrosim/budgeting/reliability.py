"""Reliability and risk budgeting."""

from __future__ import annotations

from dataclasses import dataclass, field
import math


@dataclass
class ReliabilityBudget:
    mission_hours: float
    subsystem_risks: dict[str, float] = field(default_factory=dict)

    def record_step(self, subsystem: str, outputs: dict[str, float]) -> None:
        risk = outputs.get("micrometeoroid_step_risk", 0.0)
        if risk:
            self.subsystem_risks[subsystem] = (
                self.subsystem_risks.get(subsystem, 0.0) + risk
            )

    @property
    def mission_success_probability(self) -> float:
        total_risk = sum(self.subsystem_risks.values())
        return math.exp(-total_risk)

    def summary(self) -> dict[str, float]:
        return {
            "mission_success_probability": self.mission_success_probability,
            **{f"risk_{k}": v for k, v in self.subsystem_risks.items()},
        }