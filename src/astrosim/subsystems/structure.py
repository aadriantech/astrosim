"""Structural and pressurized volume subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class StructureSubsystem(Subsystem):
    name = "structure"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        pressurized_volume_m3 = params.get("pressurized_volume_m3", 120.0)
        hull_mass_kg = params.get("hull_mass_kg", 8000.0)
        radiation_shield_kg = params.get("radiation_shield_kg", 12000.0)
        micrometeoroid_risk = params.get("micrometeoroid_annual_risk", 0.001)

        annual_hours = 8760.0
        step_risk = micrometeoroid_risk * (dt_hours / annual_hours)
        cumulative_risk = (
            self._local_state.get("micrometeoroid_cumulative_risk", 0.0) + step_risk
        )

        return {
            "pressurized_volume_m3": pressurized_volume_m3,
            "total_mass_kg": hull_mass_kg + radiation_shield_kg,
            "micrometeoroid_step_risk": step_risk,
            "micrometeoroid_cumulative_risk": cumulative_risk,
            "utilization": min(1.0, state.crew_count / max(params.get("max_crew", 6), 1)),
        }