"""Tests for NL scenario editor (offline)."""

from astrosim.ai.scenario_editor import apply_patch, parse_edit_intent


def test_parse_crew_count_intent():
    patch = parse_edit_intent("increase crew to 8")
    assert patch.simulation == {"crew_count": 8}


def test_parse_solar_array_intent():
    patch = parse_edit_intent("increase solar array to 120 kw")
    assert patch.parameters == {"solar_array_kw": 120.0}


def test_apply_patch_merges_simulation():
    scenario = {
        "name": "t",
        "location": "lunar",
        "simulation": {"duration_hours": 24, "timestep_hours": 1, "crew_count": 2},
        "parameters": {},
    }
    patch = parse_edit_intent("set crew count to 6")
    updated = apply_patch(scenario, patch)
    assert updated["simulation"]["crew_count"] == 6
    assert updated["simulation"]["duration_hours"] == 24