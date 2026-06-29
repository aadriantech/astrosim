"""Scenario loading from YAML or JSON definitions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from astrosim.engine.events import SimulationEvent
from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import Subsystem, build_subsystems


def load_scenario(path: str | Path) -> SimulationConfig:
    data = _load_data(Path(path))
    return config_from_dict(data)


def config_from_dict(data: dict[str, Any]) -> SimulationConfig:
    sim = data["simulation"]
    events = [
        SimulationEvent(
            time_hours=e["time_hours"],
            name=e["name"],
            payload=e.get("payload"),
        )
        for e in data.get("events", [])
    ]
    return SimulationConfig(
        name=data.get("name", "unnamed"),
        duration_hours=sim["duration_hours"],
        timestep_hours=sim.get("timestep_hours", 1.0),
        crew_count=sim.get("crew_count", 0),
        location=data.get("location", "unknown"),
        parameters=data.get("parameters", {}),
        events=events,
        subsystems=data.get("subsystems"),
    )


def _load_data(path: Path) -> dict[str, Any]:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def build_simulator(
    config: SimulationConfig,
    subsystems: list[Subsystem] | None = None,
) -> Simulator:
    if subsystems is None:
        subsystems = build_subsystems(config.subsystems)
    return Simulator(config, subsystems)


def load_and_build(path: str | Path) -> Simulator:
    return build_simulator(load_scenario(path))