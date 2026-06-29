"""Tests for ECLSS–greenhouse food coupling."""

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import build_subsystems


def _run_with_greenhouse(include_greenhouse: bool) -> float:
    subsystems = ["power", "eclss", "thermal"]
    if include_greenhouse:
        subsystems = ["power", "greenhouse", "eclss", "thermal"]
    config = SimulationConfig(
        name="food-loop-test",
        duration_hours=24,
        timestep_hours=6,
        crew_count=4,
        parameters={
            "solar_array_kw": 60,
            "base_load_kw": 10,
            "growth_rate_kg_per_hour": 0.5,
            "crew_tending_bonus": 0.05,
            "food_yield_fraction": 0.8,
        },
        subsystems=subsystems,
    )
    result = Simulator(config, build_subsystems(subsystems)).run()
    final = result.final_state
    assert final is not None
    return final.metrics.get("eclss.food_net_import_kg", 0.0)


def test_greenhouse_reduces_food_net_import():
    without = _run_with_greenhouse(False)
    with_gh = _run_with_greenhouse(True)
    assert with_gh < without
    assert with_gh >= 0.0