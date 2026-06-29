"""Contract tests: scenario events appear in events.yaml catalog."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "contracts" / "events.yaml"
SCENARIO_PATHS = [
    ROOT / "scenarios" / "lunar_base.yaml",
    ROOT / "scenarios" / "mars_habitat.yaml",
]


def _event_names_from_scenario(path: Path) -> set[str]:
    data = yaml.safe_load(path.read_text())
    return {event["name"] for event in data.get("events", [])}


def _catalog_event_names() -> set[str]:
    catalog = yaml.safe_load(CATALOG_PATH.read_text())
    return set(catalog["events"])


def test_lunar_scenario_events_in_catalog():
    catalog = _catalog_event_names()
    scenario_events = _event_names_from_scenario(SCENARIO_PATHS[0])
    assert scenario_events.issubset(catalog)


def test_mars_scenario_events_in_catalog():
    catalog = _catalog_event_names()
    scenario_events = _event_names_from_scenario(SCENARIO_PATHS[1])
    assert scenario_events.issubset(catalog)


def test_catalog_handlers_are_active_or_noop():
    catalog = yaml.safe_load(CATALOG_PATH.read_text())
    for name, spec in catalog["events"].items():
        assert spec["handler"] in {"active", "noop"}, f"{name} has invalid handler"


def test_noop_event_does_not_mutate_parameters():
    from astrosim.engine.events import SimulationEvent, apply_event_payload
    from astrosim.engine.state import SimulationConfig

    config = SimulationConfig(
        name="t",
        duration_hours=24,
        timestep_hours=1,
        parameters={"regolith_throughput_kg_h": 80.0},
    )
    before = dict(config.parameters)
    apply_event_payload(
        config,
        SimulationEvent(time_hours=0, name="crew_rotation", payload={"alert": 1}),
    )
    assert config.parameters == before


def test_active_isru_ramp_up_mutates_parameters():
    from astrosim.engine.events import SimulationEvent, apply_event_payload
    from astrosim.engine.state import SimulationConfig

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