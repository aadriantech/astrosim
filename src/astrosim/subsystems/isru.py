"""In-Situ Resource Utilization subsystem."""

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
        max_throughput_kg_h = params.get("regolith_throughput_kg_h", 50.0)
        o2_yield = params.get("o2_extraction_yield", 0.02)
        water_yield = params.get("water_extraction_yield", 0.005)
        base_power_kw = params.get("isru_power_kw", 8.0)
        quality = float(params.get("regolith_quality", 1.0))
        quality = max(0.0, min(1.0, quality))

        power_kwh_needed = base_power_kw * dt_hours
        available_kwh = max(0.0, state.energy_kwh + params.get("battery_kwh", 200.0))
        power_factor = min(1.0, available_kwh / max(power_kwh_needed, 0.001))

        effective_throughput = max_throughput_kg_h * quality * power_factor
        processed_kg = effective_throughput * dt_hours
        o2_produced = processed_kg * o2_yield
        water_produced = processed_kg * water_yield
        actual_power_kw = base_power_kw * power_factor

        state.mass_kg -= (o2_produced + water_produced)

        return {
            "regolith_processed_kg": processed_kg,
            "o2_produced_kg": o2_produced,
            "water_produced_kg": water_produced,
            "power_kw": actual_power_kw,
            "power_limited_factor": power_factor,
        }