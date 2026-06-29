"""Tests for built-in greenhouse subsystem."""

from astrosim.engine.state import SimulationState
from astrosim.subsystems.greenhouse import GreenhouseSubsystem


def test_greenhouse_growth_with_crew_bonus():
    gh = GreenhouseSubsystem()
    state = SimulationState(crew_count=4)
    out = gh.step(state, 12.0, {"growth_rate_kg_per_hour": 0.1, "crew_tending_bonus": 0.02})
    assert out["growth_kg"] == (0.1 + 4 * 0.02) * 12.0
    assert out["biomass_kg"] == out["growth_kg"]


def test_food_supplied_from_growth_yield():
    gh = GreenhouseSubsystem()
    state = SimulationState(crew_count=0)
    out = gh.step(state, 6.0, {"growth_rate_kg_per_hour": 0.2, "food_yield_fraction": 0.8})
    assert out["food_supplied_kg"] == out["growth_kg"] * 0.8


def test_negative_growth_rate_clamped():
    gh = GreenhouseSubsystem()
    state = SimulationState(crew_count=0)
    out = gh.step(state, 6.0, {"growth_rate_kg_per_hour": -1.0})
    assert out["growth_kg"] == 0.0