from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import DEFAULT_SUBSYSTEMS


def test_simulator_runs_all_steps():
    config = SimulationConfig(
        name="test",
        duration_hours=24,
        timestep_hours=6,
        crew_count=2,
        location="lunar",
        parameters={"solar_array_kw": 40, "base_load_kw": 10},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()

    assert len(result.history) == 4
    assert result.energy_budget is not None
    assert result.mass_budget is not None
    assert result.reliability_budget is not None
    assert result.final_state is not None
    assert "power.generated_kwh" in result.final_state.metrics


def test_final_state_is_last_history_entry():
    config = SimulationConfig(
        name="test",
        duration_hours=12,
        timestep_hours=6,
        crew_count=1,
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()

    assert result.final_state is result.history[-1]
    assert result.final_state.step == result.history[-1].step


def test_metrics_keys_prefixed_with_subsystem_field():
    config = SimulationConfig(
        name="test",
        duration_hours=6,
        timestep_hours=6,
        crew_count=1,
        parameters={"solar_array_kw": 40, "base_load_kw": 10},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
    metrics = result.final_state.metrics

    assert any(key.startswith("power.") for key in metrics)
    assert "power.generated_kwh" in metrics
    assert "power.stored_kwh" in metrics


def test_mission_success_probability_bounded():
    config = SimulationConfig(
        name="test",
        duration_hours=8760,
        timestep_hours=24,
        crew_count=1,
        parameters={"micrometeoroid_annual_risk": 0.01},
    )
    result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
    assert result.reliability_budget is not None
    p = result.reliability_budget.mission_success_probability
    assert 0.0 < p <= 1.0