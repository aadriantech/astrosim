"""Result export utilities."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from astrosim.engine.simulator import SimulationResult
from astrosim.visualization.dashboard import result_to_dataframe


def export_json(result: SimulationResult, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "config": {
            "name": result.config.name,
            "duration_hours": result.config.duration_hours,
            "timestep_hours": result.config.timestep_hours,
            "crew_count": result.config.crew_count,
            "location": result.config.location,
            "parameters": result.config.parameters,
        },
        "energy": result.energy_budget.summary() if result.energy_budget else {},
        "mass": result.mass_budget.summary() if result.mass_budget else {},
        "reliability": (
            result.reliability_budget.summary() if result.reliability_budget else {}
        ),
        "history": result_to_dataframe(result).to_dict(orient="records"),
    }

    output.write_text(json.dumps(payload, indent=2))
    return output


def export_csv(result: SimulationResult, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    result_to_dataframe(result).to_csv(output, index=False)
    return output