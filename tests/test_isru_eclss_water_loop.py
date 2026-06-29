"""Tests for ISRU–ECLSS water coupling."""

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import build_subsystems


def _final_water_net(include_isru: bool) -> float:
    subsystems = ["power", "eclss", "thermal"]
    if include_isru:
        subsystems = ["power", "isru", "eclss", "thermal"]
    config = SimulationConfig(
        name="water-loop-test",
        duration_hours=24,
        timestep_hours=6,
        crew_count=4,
        parameters={
            "solar_array_kw": 100,
            "base_load_kw": 10,
            "battery_kwh": 500,
            "regolith_throughput_kg_h": 100,
            "water_extraction_yield": 0.01,
            "isru_power_kw": 8,
        },
        subsystems=subsystems,
    )
    result = Simulator(config, build_subsystems(subsystems)).run()
    final = result.final_state
    assert final is not None
    return final.metrics.get("eclss.water_net_kg", 0.0)


def test_isru_reduces_eclss_water_net():
    without = _final_water_net(False)
    with_isru = _final_water_net(True)
    assert with_isru < without
    assert with_isru >= 0.0