"""Base subsystem interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from astrosim.engine.state import SimulationState


class Subsystem(ABC):
    """Pluggable habitat subsystem model."""

    name: str
    _local_state: dict[str, float]

    def __init__(self) -> None:
        self._local_state: dict[str, float] = {}

    @abstractmethod
    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        """Advance one timestep and return metric outputs."""

    def get_state(self) -> dict[str, float]:
        """Return the subsystem's current internal state."""
        return dict(self._local_state)

    def step(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        """Compatibility wrapper around update()."""
        outputs = self.update(state, dt_hours, params)
        self._local_state.update(outputs)
        return outputs