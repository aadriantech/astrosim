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
    if not event.payload:
        return

    if event.name == "isru_ramp_up":
        throughput = float(config.parameters.get("regolith_throughput_kg_h", 50.0))
        boost = float(event.payload.get("boost", 1.0))
        multiplier = 1.0 + (0.5 * boost)
        config.parameters["regolith_throughput_kg_h"] = throughput * multiplier
        config.parameters["isru_ramp_active"] = True