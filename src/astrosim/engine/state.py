"""Simulation state containers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from astrosim.engine.events import SimulationEvent


@dataclass
class SimulationState:
    """Mutable state passed between subsystems each timestep."""

    time_hours: float = 0.0
    step: int = 0
    energy_kwh: float = 0.0
    mass_kg: float = 0.0
    crew_count: int = 0
    subsystem_outputs: dict[str, dict[str, float]] = field(default_factory=dict)
    metrics: dict[str, float] = field(default_factory=dict)
    flags: dict[str, bool] = field(default_factory=dict)
    events_fired: list[str] = field(default_factory=list)

    def record_subsystem(self, name: str, outputs: dict[str, float]) -> None:
        self.subsystem_outputs[name] = outputs
        self.metrics.update({f"{name}.{k}": v for k, v in outputs.items()})


@dataclass
class SimulationConfig:
    """Top-level simulation parameters."""

    name: str
    duration_hours: float
    timestep_hours: float
    crew_count: int = 0
    location: str = "lunar"
    parameters: dict[str, Any] = field(default_factory=dict)
    events: list[SimulationEvent] = field(default_factory=list)
    subsystems: list[str] | None = None

    @property
    def num_steps(self) -> int:
        return max(1, int(self.duration_hours / self.timestep_hours))