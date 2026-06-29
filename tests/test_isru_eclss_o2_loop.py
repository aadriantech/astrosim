"""Tests for ISRU–ECLSS O₂ coupling."""

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import build_subsystems


def _final_o2_net(include_isru: bool) -> float:
    subsystems = ["power", "eclss", "thermal"]
    if include_isru:
        subsystems = ["power", "isru", "eclss", "thermal"]
    config = SimulationConfig(
        name="o2-loop-test",
        duration_hours=24,
        timestep_hours=6,
        crew_count=4,
        parameters={
            "solar_array_kw": 100,
            "base_load_kw": 10,
            "battery_kwh": 500,
            "regolith_throughput_kg_h": 80,
            "o2_extraction_yield": 0.03,
            "isru_power_kw": 8,
        },
        subsystems=subsystems,
    )
    result = Simulator(config, build_subsystems(subsystems)).run()
    final = result.final_state
    assert final is not None
    return final.metrics.get("eclss.o2_net_import_kg", 0.0)


def test_isru_reduces_o2_net_import():
    without = _final_o2_net(False)
    with_isru = _final_o2_net(True)
    assert with_isru < without
    assert with_isru >= 0.0