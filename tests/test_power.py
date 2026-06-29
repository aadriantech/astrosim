from astrosim.engine.state import SimulationState
from astrosim.subsystems.power import PowerSubsystem


def test_generated_kwh_equals_solar_times_cf_times_dt():
    subsystem = PowerSubsystem()
    state = SimulationState(crew_count=0)
    params = {
        "solar_array_kw": 80.0,
        "solar_capacity_factor": 0.3,
        "base_load_kw": 0.0,
    }
    dt_hours = 4.0

    outputs = subsystem.update(state, dt_hours, params)

    assert outputs["generated_kwh"] == 80.0 * 0.3 * 4.0


def test_zero_solar_positive_load_decreases_stored_energy():
    subsystem = PowerSubsystem()
    state = SimulationState(crew_count=0, energy_kwh=50.0)
    params = {
        "solar_array_kw": 0.0,
        "solar_capacity_factor": 0.25,
        "base_load_kw": 20.0,
        "battery_kwh": 200.0,
    }
    dt_hours = 2.0

    outputs = subsystem.update(state, dt_hours, params)

    assert outputs["generated_kwh"] == 0.0
    assert outputs["consumed_kwh"] > 0.0
    assert outputs["stored_kwh"] < 50.0


def test_stored_energy_clamped_to_battery_capacity():
    subsystem = PowerSubsystem()
    battery_kwh = 100.0
    params = {
        "solar_array_kw": 200.0,
        "solar_capacity_factor": 1.0,
        "base_load_kw": 0.0,
        "battery_kwh": battery_kwh,
    }
    dt_hours = 10.0

    state_high = SimulationState(crew_count=0, energy_kwh=90.0)
    outputs_high = subsystem.update(state_high, dt_hours, params)
    assert -battery_kwh <= outputs_high["stored_kwh"] <= battery_kwh

    state_low = SimulationState(crew_count=0, energy_kwh=-90.0)
    params["solar_array_kw"] = 0.0
    params["base_load_kw"] = 50.0
    outputs_low = subsystem.update(state_low, dt_hours, params)
    assert -battery_kwh <= outputs_low["stored_kwh"] <= battery_kwh


def test_crew_adds_half_kw_per_person():
    subsystem = PowerSubsystem()
    state = SimulationState(crew_count=4)
    params = {"base_load_kw": 10.0}

    outputs = subsystem.update(state, 1.0, params)

    assert outputs["load_kw"] == 10.0 + 4 * 0.5