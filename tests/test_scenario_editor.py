"""Tests for NL scenario editor (offline)."""

from pathlib import Path

import pytest

from astrosim.ai.scenario_editor import apply_patch, parse_edit_intent
from astrosim.cli import handle_ask

ROOT = Path(__file__).resolve().parent.parent


def test_parse_crew_count_intent():
    patch = parse_edit_intent("increase crew to 8")
    assert patch.simulation == {"crew_count": 8}


def test_parse_solar_array_intent():
    patch = parse_edit_intent("increase solar array to 120 kw")
    assert patch.parameters == {"solar_array_kw": 120.0}


def test_parse_battery_and_duration():
    patch = parse_edit_intent("set battery storage to 500 kwh and set duration to 720 hours")
    assert patch.parameters == {"battery_kwh": 500.0}
    assert patch.simulation == {"duration_hours": 720.0}


def test_parse_regolith_throughput_intent():
    patch = parse_edit_intent("set regolith throughput to 90 kg/h")
    assert patch.parameters == {"regolith_throughput_kg_h": 90.0}


def test_parse_isru_power_intent():
    patch = parse_edit_intent("set isru power to 18 kw")
    assert patch.parameters == {"isru_power_kw": 18.0}


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


def test_handle_ask_write_creates_patched_file(tmp_path):
    src = tmp_path / "demo.yaml"
    src.write_text((ROOT / "scenarios" / "lunar_base.yaml").read_text())
    out = tmp_path / "demo.patched.yaml"
    handle_ask(src, "set crew count to 6", write=True, output=out)
    assert out.exists()
    assert "crew_count: 6" in out.read_text()


def test_handle_ask_write_refuses_overwrite(tmp_path):
    src = tmp_path / "demo.yaml"
    src.write_text((ROOT / "scenarios" / "lunar_base.yaml").read_text())
    out = tmp_path / "demo.patched.yaml"
    out.write_text("existing")
    with pytest.raises(SystemExit):
        handle_ask(src, "set crew count to 6", write=True, output=out, force=False)