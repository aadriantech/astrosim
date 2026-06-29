from astrosim.ai.hooks import AIHooks, InsightRequest
from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import DEFAULT_SUBSYSTEMS


def _run_scenario(**overrides):
    params = {
        "solar_array_kw": 40,
        "base_load_kw": 10,
        **overrides,
    }
    config = SimulationConfig(
        name="ai-hooks-test",
        duration_hours=24,
        timestep_hours=6,
        crew_count=2,
        parameters=params,
    )
    return Simulator(config, DEFAULT_SUBSYSTEMS).run()


def test_offline_insights_are_non_empty():
    result = _run_scenario()
    insights = AIHooks().generate_insights(InsightRequest(result=result))

    assert insights
    assert len(insights.strip()) > 0
    assert "ai-hooks-test" in insights


def test_energy_deficit_triggers_solar_suggestion():
    result = _run_scenario(solar_array_kw=5, base_load_kw=40)
    suggestions = AIHooks().suggest_optimizations(result)

    solar = [s for s in suggestions if s.parameter == "solar_array_kw"]
    assert solar
    assert solar[0].suggested_value > solar[0].current_value
    assert "Energy deficit" in solar[0].rationale


def test_mass_import_triggers_water_recovery_suggestion():
    result = _run_scenario(
        water_recovery_rate=0.85,
        regolith_throughput_kg_h=0.0,
        water_kg_per_person_day=5.0,
    )
    assert result.mass_budget is not None
    assert result.mass_budget.net_import_kg > 0

    suggestions = AIHooks().suggest_optimizations(result)

    recovery = [s for s in suggestions if s.parameter == "water_recovery_rate"]
    assert recovery
    assert recovery[0].suggested_value > recovery[0].current_value
    assert "mass import" in recovery[0].rationale.lower()