#!/usr/bin/env python3
"""Minimal custom subsystem demo using @register_subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationConfig, SimulationState
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import (
    Subsystem,
    build_subsystems,
    register_subsystem,
    unregister_subsystem,
)


@register_subsystem
class GreenhouseSubsystem(Subsystem):
    """Simple biomass growth model for demonstration."""

    name = "greenhouse"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        rate = params.get("growth_rate_kg_per_hour", 0.05)
        crew_bonus = state.crew_count * params.get("crew_tending_bonus", 0.01)
        biomass = self._local_state.get("biomass_kg", 0.0) + (rate + crew_bonus) * dt_hours
        return {"biomass_kg": biomass, "growth_kg": (rate + crew_bonus) * dt_hours}


def main() -> None:
    config = SimulationConfig(
        name="Greenhouse Demo",
        duration_hours=48,
        timestep_hours=12,
        crew_count=2,
        location="lunar",
        parameters={
            "solar_array_kw": 30,
            "base_load_kw": 8,
            "growth_rate_kg_per_hour": 0.1,
            "crew_tending_bonus": 0.02,
        },
        subsystems=["power", "greenhouse"],
    )

    subsystems = build_subsystems(config.subsystems)
    result = Simulator(config, subsystems).run()

    final = result.final_state
    assert final is not None
    print(f"Scenario: {config.name}")
    print(f"Steps: {len(result.history)}")
    print(f"Final biomass: {final.metrics.get('greenhouse.biomass_kg', 0):.2f} kg")
    print(f"Registered subsystems: {config.subsystems}")


if __name__ == "__main__":
    try:
        main()
    finally:
        unregister_subsystem("greenhouse")