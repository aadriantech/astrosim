"""Tests for ECLSS subsystem (SRD 2.2.1.7-10)."""

import pytest

from astrosim.engine.state import SimulationState
from astrosim.subsystems.eclss import ECLSSSubsystem


def test_o2_consumption_two_crew_one_day():
    """2.2.1.7: O2 consumed for 2 crew over 1 day."""
    eclss = ECLSSSubsystem()
    state = SimulationState(crew_count=2)

    result = eclss.update(state, 24.0, {"o2_kg_per_person_day": 0.84})

    assert result["o2_consumed_kg"] == pytest.approx(2 * 0.84 * 1.0)


def test_water_net_with_recovery_rate():
    """2.2.1.8-9: water_net reflects consumption minus recovery."""
    eclss = ECLSSSubsystem()
    state = SimulationState(crew_count=2)
    recovery_rate = 0.93

    result = eclss.update(
        state,
        24.0,
        {
            "water_kg_per_person_day": 3.0,
            "water_recovery_rate": recovery_rate,
        },
    )

    water_consumed = 2 * 3.0 * 1.0
    expected_net = water_consumed * (1.0 - recovery_rate)

    assert result["water_net_kg"] == pytest.approx(expected_net)


def test_co2_rises_over_time():
    """2.2.1.10: CO2 concentration rises across timesteps."""
    eclss = ECLSSSubsystem()
    state = SimulationState(crew_count=2)

    first = eclss.step(state, 24.0, {"co2_ppm": 400.0})
    second = eclss.step(state, 24.0, {})

    assert second["co2_ppm"] > first["co2_ppm"]