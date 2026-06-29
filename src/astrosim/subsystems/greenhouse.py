"""Greenhouse biomass and food production subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class GreenhouseSubsystem(Subsystem):
    name = "greenhouse"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        rate = max(0.0, params.get("growth_rate_kg_per_hour", 0.05))
        crew_bonus = state.crew_count * params.get("crew_tending_bonus", 0.01)
        growth_kg = (rate + crew_bonus) * dt_hours
        biomass_kg = self._local_state.get("biomass_kg", 0.0) + growth_kg
        food_yield = max(0.0, min(1.0, params.get("food_yield_fraction", 0.8)))
        food_supplied_kg = growth_kg * food_yield
        power_kw = params.get("greenhouse_power_kw", 1.5)

        return {
            "biomass_kg": biomass_kg,
            "growth_kg": growth_kg,
            "food_supplied_kg": food_supplied_kg,
            "power_kw": power_kw,
        }