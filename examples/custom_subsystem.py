#!/usr/bin/env python3
"""Custom subsystem plugin demo (built-in greenhouse + ephemeral beacon plugin)."""

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
class DemoBeaconSubsystem(Subsystem):
    """Ephemeral plugin for register/unregister smoke."""

    name = "demo_beacon"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        pulses = self._local_state.get("pulses", 0.0) + 1.0
        return {"pulses": pulses, "power_kw": params.get("beacon_power_kw", 0.1)}


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
            "beacon_power_kw": 0.05,
        },
        subsystems=["power", "greenhouse", "demo_beacon"],
    )

    subsystems = build_subsystems(config.subsystems)
    result = Simulator(config, subsystems).run()

    final = result.final_state
    assert final is not None
    print(f"Scenario: {config.name}")
    print(f"Steps: {len(result.history)}")
    print(f"Final biomass: {final.metrics.get('greenhouse.biomass_kg', 0):.2f} kg")
    print(f"Beacon pulses: {final.metrics.get('demo_beacon.pulses', 0):.0f}")
    print(f"Registered subsystems: {config.subsystems}")


if __name__ == "__main__":
    try:
        main()
    finally:
        unregister_subsystem("demo_beacon")