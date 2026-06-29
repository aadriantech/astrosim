import pytest

from astrosim.budgeting.mass import MassBudget


def test_accumulate_tracks_produced_and_consumed():
    budget = MassBudget()
    budget.accumulate("isru", {"o2_produced_kg": 2.0, "water_produced_kg": 1.0})
    budget.accumulate(
        "eclss",
        {
            "o2_consumed_kg": 1.0,
            "water_net_kg": 0.5,
            "food_consumed_kg": 0.3,
        },
    )

    assert budget.produced_kg == 3.0
    assert budget.consumed_kg == pytest.approx(1.8)


def test_net_import_kg_equals_consumed_minus_produced_plus_imported():
    budget = MassBudget(imported_kg=10.0, produced_kg=5.0, consumed_kg=20.0)

    assert budget.net_import_kg == 25.0


def test_summary_returns_expected_keys():
    budget = MassBudget(imported_kg=1.0, produced_kg=2.0, consumed_kg=3.0)

    summary = budget.summary()

    assert set(summary.keys()) == {
        "imported_kg",
        "produced_kg",
        "consumed_kg",
        "net_import_kg",
    }
    assert summary["net_import_kg"] == 2.0