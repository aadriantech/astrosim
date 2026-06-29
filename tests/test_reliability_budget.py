import math

import pytest

from astrosim.budgeting.reliability import ReliabilityBudget


def test_record_step_accumulates_subsystem_risk():
    budget = ReliabilityBudget(mission_hours=8760)
    budget.record_step("structure", {"micrometeoroid_step_risk": 0.001})
    budget.record_step("structure", {"micrometeoroid_step_risk": 0.002})

    assert budget.subsystem_risks["structure"] == pytest.approx(0.003)


def test_mission_success_probability_is_exp_negative_total_risk():
    budget = ReliabilityBudget(mission_hours=8760)
    budget.record_step("structure", {"micrometeoroid_step_risk": 0.1})

    assert budget.mission_success_probability == pytest.approx(math.exp(-0.1))


def test_summary_includes_probability_and_per_subsystem_risks():
    budget = ReliabilityBudget(mission_hours=8760)
    budget.record_step("structure", {"micrometeoroid_step_risk": 0.05})

    summary = budget.summary()

    assert summary["mission_success_probability"] == pytest.approx(math.exp(-0.05))
    assert summary["risk_structure"] == pytest.approx(0.05)