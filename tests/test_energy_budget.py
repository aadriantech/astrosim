from astrosim.budgeting.energy import EnergyBudget


def test_net_kwh_equals_generated_minus_consumed():
    budget = EnergyBudget(generated_kwh=120.0, consumed_kwh=45.0)

    assert budget.net_kwh == 75.0


def test_by_subsystem_tracks_eclss_power_draw():
    budget = EnergyBudget()
    outputs = {
        "power_kw": 2.0,
        "consumed_kwh": 4.0,
        "load_kw": 2.0,
    }

    budget.accumulate("eclss", outputs)

    assert budget.by_subsystem["eclss"] == 4.0


def test_summary_returns_expected_keys():
    budget = EnergyBudget(generated_kwh=50.0, consumed_kwh=30.0)

    summary = budget.summary()

    assert set(summary.keys()) == {"generated_kwh", "consumed_kwh", "net_kwh"}
    assert summary["generated_kwh"] == 50.0
    assert summary["consumed_kwh"] == 30.0
    assert summary["net_kwh"] == 20.0