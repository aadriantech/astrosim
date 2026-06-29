"""Thermal management subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class ThermalSubsystem(Subsystem):
    name = "thermal"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        ambient_c = params.get("ambient_temp_c", -20.0)
        internal_target_c = params.get("internal_target_c", 22.0)
        heat_load_kw = params.get("internal_heat_kw", 5.0) + state.crew_count * 0.1
        radiator_efficiency = params.get("radiator_efficiency", 0.85)

        delta_t = internal_target_c - ambient_c
        rejection_kw = heat_load_kw * radiator_efficiency
        pump_power_kw = params.get("pump_power_kw", 0.5) + delta_t * 0.01

        return {
            "heat_load_kw": heat_load_kw,
            "rejection_kw": rejection_kw,
            "pump_power_kw": pump_power_kw,
            "delta_t_c": delta_t,
        }