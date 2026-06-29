"""Event-driven simulation triggers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from astrosim.engine.state import SimulationConfig


@dataclass(frozen=True)
class SimulationEvent:
    """A scheduled event that fires at a specific simulation time."""

    time_hours: float
    name: str
    handler: Callable[[], None] | None = None
    payload: dict[str, float] | None = None


class EventQueue:
    """Sorted queue of simulation events."""

    def __init__(self, events: list[SimulationEvent] | None = None) -> None:
        self._events = sorted(events or [], key=lambda e: e.time_hours)

    def due_at(self, time_hours: float, tolerance: float = 1e-9) -> list[SimulationEvent]:
        due: list[SimulationEvent] = []
        remaining: list[SimulationEvent] = []
        for event in self._events:
            if abs(event.time_hours - time_hours) <= tolerance:
                due.append(event)
            else:
                remaining.append(event)
        self._events = remaining
        return due

    def __len__(self) -> int:
        return len(self._events)


def apply_event_payload(config: SimulationConfig, event: SimulationEvent) -> None:
    """Apply declarative event effects to the live simulation configuration."""
    payload = event.payload or {}

    if event.name == "isru_ramp_up":
        throughput = float(config.parameters.get("regolith_throughput_kg_h", 50.0))
        boost = float(payload.get("boost", 1.0))
        multiplier = 1.0 + (0.5 * boost)
        config.parameters["regolith_throughput_kg_h"] = throughput * multiplier
        config.parameters["isru_ramp_active"] = True
        return

    if event.name == "dust_storm":
        capacity_factor = float(config.parameters.get("solar_capacity_factor", 0.25))
        if "severity" in payload:
            severity = float(payload["severity"])
        else:
            severity = float(payload.get("alert", 1.0)) * 0.3
        severity = max(0.0, min(1.0, severity))
        config.parameters["solar_capacity_factor"] = capacity_factor * (1.0 - 0.5 * severity)
        config.parameters["dust_storm_active"] = True
        return

    if event.name == "crew_rotation":
        config.parameters["crew_rotation_active"] = True
        recovery = float(config.parameters.get("water_recovery_rate", 0.93))
        config.parameters["water_recovery_rate"] = min(0.99, recovery + 0.02)
        return