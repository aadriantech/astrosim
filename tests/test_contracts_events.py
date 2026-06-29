"""Contract tests: scenario events appear in events.yaml catalog."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from astrosim.engine.events import SimulationEvent, apply_event_payload
from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import build_subsystems

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "contracts" / "events.yaml"
SCENARIO_PATHS = [
    ROOT / "scenarios" / "lunar_base.yaml",
    ROOT / "scenarios" / "lunar_base.json",
    ROOT / "scenarios" / "mars_habitat.yaml",
    ROOT / "scenarios" / "mars_habitat.json",
]


def _load_scenario_dict(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _event_names_from_scenario(path: Path) -> set[str]:
    data = _load_scenario_dict(path)
    return {event["name"] for event in data.get("events", [])}


def _catalog_event_names() -> set[str]:
    catalog = yaml.safe_load(CATALOG_PATH.read_text())
    return set(catalog["events"])


@pytest.mark.parametrize("scenario_path", SCENARIO_PATHS)
def test_scenario_events_in_catalog(scenario_path):
    catalog = _catalog_event_names()
    scenario_events = _event_names_from_scenario(scenario_path)
    assert scenario_events.issubset(catalog)


def test_catalog_handlers_are_active_or_noop():
    catalog = yaml.safe_load(CATALOG_PATH.read_text())
    for name, spec in catalog["events"].items():
        assert spec["handler"] in {"active", "noop"}, f"{name} has invalid handler"


def test_crew_rotation_mutates_recovery_rate():
    config = SimulationConfig(
        name="t",
        duration_hours=24,
        timestep_hours=1,
        parameters={"water_recovery_rate": 0.94},
    )
    apply_event_payload(
        config,
        SimulationEvent(time_hours=0, name="crew_rotation", payload={"alert": 1}),
    )
    assert config.parameters["crew_rotation_active"] is True
    assert config.parameters["water_recovery_rate"] == 0.96


def test_dust_storm_reduces_solar_capacity_factor():
    config = SimulationConfig(
        name="t",
        duration_hours=24,
        timestep_hours=1,
        parameters={"solar_capacity_factor": 0.2},
    )
    apply_event_payload(
        config,
        SimulationEvent(time_hours=0, name="dust_storm", payload={"alert": 1}),
    )
    assert config.parameters["dust_storm_active"] is True
    assert config.parameters["solar_capacity_factor"] == pytest.approx(0.17)


def test_active_isru_ramp_up_mutates_parameters():
    config = SimulationConfig(
        name="t",
        duration_hours=24,
        timestep_hours=1,
        parameters={"regolith_throughput_kg_h": 80.0},
    )
    apply_event_payload(
        config,
        SimulationEvent(time_hours=0, name="isru_ramp_up", payload={"boost": 1}),
    )
    assert config.parameters["isru_ramp_active"] is True
    assert config.parameters["regolith_throughput_kg_h"] == 120.0


def test_dust_storm_reduces_power_generation_in_simulation():
    config = SimulationConfig(
        name="dust",
        duration_hours=24,
        timestep_hours=12,
        crew_count=0,
        parameters={"solar_array_kw": 100, "solar_capacity_factor": 0.2, "base_load_kw": 0},
        events=[SimulationEvent(time_hours=12, name="dust_storm", payload={"severity": 1.0})],
    )
    result = Simulator(config, build_subsystems(["power"])).run()
    before = result.history[0].metrics["power.generated_kwh"]
    after = result.history[1].metrics["power.generated_kwh"]
    assert after < before