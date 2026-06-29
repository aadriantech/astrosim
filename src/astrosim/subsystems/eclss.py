"""Environmental Control and Life Support System."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class ECLSSSubsystem(Subsystem):
    name = "eclss"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        o2_kg_per_person_day = params.get("o2_kg_per_person_day", 0.84)
        water_kg_per_person_day = params.get("water_kg_per_person_day", 3.0)
        food_kg_per_person_day = params.get("food_kg_per_person_day", 1.8)
        waste_kg_per_person_day = params.get("waste_kg_per_person_day", 0.5)
        water_recovery_rate = params.get("water_recovery_rate", 0.93)
        waste_recovery_rate = params.get("waste_recovery_rate", 0.75)
        co2_ppm = self._local_state.get("co2_ppm", params.get("co2_ppm", 400.0))

        crew = max(state.crew_count, 1)
        days = dt_hours / 24.0

        o2_consumed = crew * o2_kg_per_person_day * days
        water_consumed = crew * water_kg_per_person_day * days
        food_consumed = crew * food_kg_per_person_day * days
        waste_generated = crew * waste_kg_per_person_day * days

        water_recovered = water_consumed * water_recovery_rate
        waste_recycled = waste_generated * waste_recovery_rate
        water_net = water_consumed - water_recovered
        waste_net = waste_generated - waste_recycled
        co2_ppm += crew * 50.0 * days

        state.mass_kg += water_net + food_consumed - waste_recycled

        return {
            "o2_consumed_kg": o2_consumed,
            "water_consumed_kg": water_consumed,
            "water_recovered_kg": water_recovered,
            "water_net_kg": water_net,
            "food_consumed_kg": food_consumed,
            "waste_generated_kg": waste_generated,
            "waste_recycled_kg": waste_recycled,
            "waste_net_kg": waste_net,
            "co2_ppm": co2_ppm,
            "power_kw": params.get("eclss_power_kw", 2.0),
        }