"""Tests for compute subsystem (SRD 2.4.1.5-7)."""

import pytest

from astrosim.engine.state import SimulationState
from astrosim.subsystems.compute import ComputeSubsystem


def test_power_scales_with_ai_utilization():
    """2.4.1.5-6: compute power draw scales with AI utilization."""
    compute = ComputeSubsystem()
    state = SimulationState()
    base_params = {"compute_nodes": 4, "watts_per_node": 100.0}

    low = compute.update(state, 1.0, {**base_params, "ai_utilization": 0.3})
    high = compute.update(state, 1.0, {**base_params, "ai_utilization": 0.9})

    assert high["power_kw"] > low["power_kw"]
    assert high["power_kw"] == pytest.approx(3.0 * low["power_kw"])


def test_shielding_reduces_dose():
    """2.4.1.7: radiation shielding reduces per-step dose."""
    compute = ComputeSubsystem()
    state = SimulationState()
    dose_params = {"radiation_sv_per_year": 0.5}

    unshielded = compute.update(
        state,
        8760.0,
        {**dose_params, "compute_shielding_factor": 0.0},
    )
    shielded = compute.update(
        state,
        8760.0,
        {**dose_params, "compute_shielding_factor": 0.8},
    )

    assert shielded["dose_sv_step"] < unshielded["dose_sv_step"]