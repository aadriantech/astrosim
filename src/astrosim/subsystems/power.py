"""Power generation and distribution subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class PowerSubsystem(Subsystem):
    name = "power"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        solar_kw = params.get("solar_array_kw", 50.0)
        capacity_factor = params.get("solar_capacity_factor", 0.25)
        battery_kwh = params.get("battery_kwh", 200.0)
        load_kw = params.get("base_load_kw", 15.0) + state.crew_count * 0.5

        generated_kwh = solar_kw * capacity_factor * dt_hours
        consumed_kwh = load_kw * dt_hours
        net_kwh = generated_kwh - consumed_kwh

        state.energy_kwh = max(
            -battery_kwh,
            min(battery_kwh, state.energy_kwh + net_kwh),
        )

        return {
            "generated_kwh": generated_kwh,
            "consumed_kwh": consumed_kwh,
            "stored_kwh": state.energy_kwh,
            "load_kw": load_kw,
        }