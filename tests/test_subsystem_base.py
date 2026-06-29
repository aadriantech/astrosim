import pytest

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem
from astrosim.subsystems.eclss import ECLSSSubsystem


def test_incomplete_subclass_raises_type_error():
    class IncompleteSubsystem(Subsystem):
        name = "incomplete"

    with pytest.raises(TypeError):
        IncompleteSubsystem()


def test_get_state_returns_copy_after_update():
    subsystem = ECLSSSubsystem()
    state = SimulationState(crew_count=2)

    subsystem.step(state, 24.0, {})
    internal = subsystem.get_state()

    internal["food_consumed_kg"] = -1.0

    assert subsystem.get_state()["food_consumed_kg"] != -1.0