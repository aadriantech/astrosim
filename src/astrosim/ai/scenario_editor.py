"""Natural-language scenario edit intents (offline heuristic parser)."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ScenarioPatch:
    """Structured edits to apply to a scenario dict."""

    simulation: dict[str, float | int] | None = None
    parameters: dict[str, float] | None = None
    dry_run: bool = True


_CREW_RE = re.compile(r"(?:increase|set|raise)\s+crew(?:\s+count)?\s+to\s+(\d+)", re.I)
_SOLAR_RE = re.compile(r"(?:increase|set|raise)\s+solar(?:\s+array)?\s+(?:to\s+)?(\d+(?:\.\d+)?)\s*kw", re.I)
_BATTERY_RE = re.compile(r"(?:increase|set|raise)\s+battery(?:\s+storage)?\s+(?:to\s+)?(\d+(?:\.\d+)?)\s*kwh", re.I)
_DURATION_RE = re.compile(r"(?:set|run)\s+duration\s+(?:to\s+)?(\d+(?:\.\d+)?)\s*h(?:ours)?", re.I)


def parse_edit_intent(prompt: str) -> ScenarioPatch:
    """Parse simple NL edit requests without calling an LLM."""
    text = prompt.strip()
    patch = ScenarioPatch()

    simulation: dict[str, float | int] = dict(patch.simulation or {})
    parameters: dict[str, float] = dict(patch.parameters or {})

    crew_match = _CREW_RE.search(text)
    if crew_match:
        simulation["crew_count"] = int(crew_match.group(1))

    duration_match = _DURATION_RE.search(text)
    if duration_match:
        simulation["duration_hours"] = float(duration_match.group(1))

    solar_match = _SOLAR_RE.search(text)
    if solar_match:
        parameters["solar_array_kw"] = float(solar_match.group(1))

    battery_match = _BATTERY_RE.search(text)
    if battery_match:
        parameters["battery_kwh"] = float(battery_match.group(1))

    if simulation:
        patch.simulation = simulation
    if parameters:
        patch.parameters = parameters

    return patch


def apply_patch(scenario: dict, patch: ScenarioPatch) -> dict:
    """Return a new scenario dict with patch applied (non-destructive)."""
    updated = dict(scenario)
    if patch.simulation:
        sim = dict(updated.get("simulation", {}))
        sim.update(patch.simulation)
        updated["simulation"] = sim
    if patch.parameters:
        params = dict(updated.get("parameters", {}))
        params.update(patch.parameters)
        updated["parameters"] = params
    return updated