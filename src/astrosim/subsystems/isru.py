"""PLACEHOLDER: In-Situ Resource Utilization subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class ISRUSubsystem(Subsystem):
    name = "isru"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        regolith_throughput_kg_h = params.get("regolith_throughput_kg_h", 50.0)
        o2_yield = params.get("o2_extraction_yield", 0.02)
        water_yield = params.get("water_extraction_yield", 0.005)
        power_kw = params.get("isru_power_kw", 8.0)

        processed_kg = regolith_throughput_kg_h * dt_hours
        o2_produced = processed_kg * o2_yield
        water_produced = processed_kg * water_yield

        state.mass_kg -= (o2_produced + water_produced)

        return {
            "regolith_processed_kg": processed_kg,
            "o2_produced_kg": o2_produced,
            "water_produced_kg": water_produced,
            "power_kw": power_kw,
        }