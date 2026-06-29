"""Tests for ISRU subsystem (SRD 2.3.1.4-5)."""

import pytest

from astrosim.engine.state import SimulationState
from astrosim.subsystems.isru import ISRUSubsystem


def test_processed_kg_equals_throughput_times_dt():
    """2.3.1.4: regolith processed equals throughput × dt."""
    isru = ISRUSubsystem()
    state = SimulationState()
    throughput = 50.0
    dt_hours = 10.0

    result = isru.update(state, dt_hours, {"regolith_throughput_kg_h": throughput})

    assert result["regolith_processed_kg"] == pytest.approx(throughput * dt_hours)


def test_o2_produced_equals_processed_times_yield():
    """2.3.1.5: O2 produced equals processed mass × extraction yield."""
    isru = ISRUSubsystem()
    state = SimulationState()
    throughput = 100.0
    dt_hours = 5.0
    o2_yield = 0.02

    result = isru.update(
        state,
        dt_hours,
        {
            "regolith_throughput_kg_h": throughput,
            "o2_extraction_yield": o2_yield,
        },
    )

    processed = throughput * dt_hours
    assert result["o2_produced_kg"] == pytest.approx(processed * o2_yield)