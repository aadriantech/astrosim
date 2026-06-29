"""Tests for thermal subsystem (SRD 2.1.1.6-8)."""

import pytest

from astrosim.engine.state import SimulationState
from astrosim.subsystems.thermal import ThermalSubsystem


def test_colder_ambient_increases_delta_t():
    """2.1.1.6: colder ambient temperature yields higher delta_t."""
    thermal = ThermalSubsystem()
    state = SimulationState(crew_count=2)
    params = {"internal_target_c": 22.0}

    cold = thermal.update(state, 1.0, {**params, "ambient_temp_c": -80.0})
    warm = thermal.update(state, 1.0, {**params, "ambient_temp_c": -20.0})

    assert cold["delta_t_c"] > warm["delta_t_c"]


def test_more_crew_increases_heat_load():
    """2.1.1.7-8: more crew members increase internal heat load."""
    thermal = ThermalSubsystem()
    params = {"internal_heat_kw": 5.0}

    few_crew = thermal.update(SimulationState(crew_count=2), 1.0, params)
    many_crew = thermal.update(SimulationState(crew_count=6), 1.0, params)

    assert many_crew["heat_load_kw"] > few_crew["heat_load_kw"]