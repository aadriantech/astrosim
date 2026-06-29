import json
from pathlib import Path

from astrosim.analysis.sensitivity import one_at_a_time_sensitivity
from astrosim.engine.events import SimulationEvent
from astrosim.engine.state import SimulationConfig, SimulationState
from astrosim.engine.simulator import Simulator
from astrosim.scenario import config_from_dict, load_scenario
from astrosim.subsystems import (
    build_subsystems,
    list_subsystems,
    register_subsystem,
    unregister_subsystem,
)
from astrosim.subsystems.base import Subsystem
from astrosim.subsystems.compute import ComputeSubsystem
from astrosim.subsystems.eclss import ECLSSSubsystem
from astrosim.subsystems.registry import get_subsystem
from astrosim.visualization.web import render_web_dashboard

ROOT = Path(__file__).resolve().parent.parent


def test_plugin_registry_lists_builtins():
    names = list_subsystems()
    assert "power" in names
    assert "eclss" in names
    assert len(build_subsystems()) == len(names)


def test_unregister_unknown_subsystem_is_noop():
    builtin_count = len(list_subsystems())
    unregister_subsystem("nonexistent_plugin_xyz")
    assert len(list_subsystems()) == builtin_count


def test_custom_subsystem_plugin():
    builtin_count = len(list_subsystems())

    @register_subsystem
    class DummySubsystem(Subsystem):
        name = "dummy_test"

        def update(self, state, dt_hours, params):
            return {"value": 1.0}

    try:
        assert get_subsystem("dummy_test").name == "dummy_test"
        assert len(list_subsystems()) == builtin_count + 1
    finally:
        unregister_subsystem("dummy_test")

    assert len(list_subsystems()) == builtin_count
    assert "dummy_test" not in list_subsystems()


def test_event_driven_updates():
    config = SimulationConfig(
        name="events",
        duration_hours=24,
        timestep_hours=12,
        crew_count=1,
        events=[SimulationEvent(time_hours=12, name="solar_eclipse", payload={"dark": 1})],
    )
    result = Simulator(config, build_subsystems(["power", "eclss"])).run()
    fired = [e for s in result.history for e in s.events_fired]
    assert "solar_eclipse" in fired


def test_isru_ramp_up_boosts_throughput():
    config = SimulationConfig(
        name="isru-ramp",
        duration_hours=24,
        timestep_hours=12,
        crew_count=1,
        parameters={"regolith_throughput_kg_h": 100.0},
        events=[SimulationEvent(time_hours=12, name="isru_ramp_up", payload={"boost": 1})],
    )
    result = Simulator(config, build_subsystems(["isru"])).run()
    before = [
        s.metrics.get("isru.regolith_processed_kg", 0.0)
        for s in result.history
        if s.time_hours < 12
    ]
    after = [
        s.metrics.get("isru.regolith_processed_kg", 0.0)
        for s in result.history
        if s.time_hours >= 12
    ]
    assert max(after) > max(before)
    assert config.parameters["regolith_throughput_kg_h"] == 150.0


def test_eclss_food_and_waste():
    config = SimulationConfig(
        name="eclss",
        duration_hours=24,
        timestep_hours=24,
        crew_count=2,
        parameters={"food_kg_per_person_day": 2.0, "waste_kg_per_person_day": 0.6},
    )
    result = Simulator(config, [ECLSSSubsystem()]).run()
    metrics = result.final_state.metrics
    assert metrics["eclss.food_consumed_kg"] == 4.0
    assert metrics["eclss.waste_generated_kg"] > 0


def test_compute_radiation_model():
    config = SimulationConfig(
        name="compute",
        duration_hours=8760,
        timestep_hours=8760,
        parameters={"radiation_sv_per_year": 0.5, "compute_shielding_factor": 0.5},
    )
    result = Simulator(config, [ComputeSubsystem()]).run()
    assert result.final_state.metrics["compute.cumulative_dose_sv"] > 0
    assert result.final_state.metrics["compute.bit_error_rate"] >= 0


def test_json_scenario_loading():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.json")
    assert config.name == "Lunar Base Alpha"
    assert config.parameters["solar_array_kw"] == 80


def test_config_from_dict():
    data = json.loads((ROOT / "scenarios" / "lunar_base.json").read_text())
    config = config_from_dict(data)
    assert len(config.events) == 2


def test_sensitivity_analysis():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    from astrosim.scenario import build_simulator

    result = one_at_a_time_sensitivity(
        config,
        build_simulator,
        parameter="solar_array_kw",
        metric_key="energy.net_kwh",
        num_points=5,
    )
    assert len(result.perturbations) == 5
    assert result.parameter == "solar_array_kw"


def test_web_dashboard_generation(tmp_path):
    config = SimulationConfig(
        name="web test",
        duration_hours=12,
        timestep_hours=6,
        crew_count=1,
    )
    result = Simulator(config, build_subsystems()).run()
    path = render_web_dashboard(result, tmp_path / "dash.html")
    content = path.read_text()
    assert "AstroSim Dashboard" in content
    assert "web test" in content
    assert "eclss_water_net" in content
    assert "thermal_heat_load" in content
    assert "subsystem-chart" in content


def test_subsystem_get_state():
    eclss = ECLSSSubsystem()
    config = SimulationConfig(
        name="state",
        duration_hours=24,
        timestep_hours=24,
        crew_count=1,
    )
    state = SimulationState(crew_count=1)
    eclss.step(state, 24, {})
    internal = eclss.get_state()
    assert "food_consumed_kg" in internal