"""Tests for structure subsystem (SRD 2.5.1.3)."""

from astrosim.engine.state import SimulationState
from astrosim.subsystems.structure import StructureSubsystem


def test_micrometeoroid_risk_accumulates():
    """2.5.1.3: micrometeoroid risk accumulates across timesteps."""
    structure = StructureSubsystem()
    state = SimulationState(crew_count=4)
    params = {"micrometeoroid_annual_risk": 0.001}

    first = structure.step(state, 24.0, params)
    second = structure.step(state, 24.0, params)

    assert second["micrometeoroid_cumulative_risk"] > first["micrometeoroid_cumulative_risk"]
    assert second["micrometeoroid_cumulative_risk"] == (
        first["micrometeoroid_step_risk"] + second["micrometeoroid_step_risk"]
    )