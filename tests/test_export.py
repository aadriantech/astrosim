import json
from pathlib import Path

import pandas as pd

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.export.formats import export_csv, export_json
from astrosim.subsystems import DEFAULT_SUBSYSTEMS

ROOT = Path(__file__).resolve().parent.parent


def _run_short_simulation():
    config = SimulationConfig(
        name="export-test",
        duration_hours=12,
        timestep_hours=6,
        crew_count=2,
        parameters={"solar_array_kw": 40, "base_load_kw": 10},
    )
    return Simulator(config, DEFAULT_SUBSYSTEMS).run()


def test_export_json_round_trip_structure(tmp_path):
    result = _run_short_simulation()
    path = export_json(result, tmp_path / "results.json")
    data = json.loads(path.read_text())

    assert data["config"]["name"] == "export-test"
    assert data["config"]["crew_count"] == 2
    assert set(data.keys()) == {"config", "energy", "mass", "reliability", "history"}
    assert isinstance(data["history"], list)
    assert len(data["history"]) == len(result.history)
    assert "net_kwh" in data["energy"]
    assert "net_import_kg" in data["mass"]
    assert "mission_success_probability" in data["reliability"]


def test_export_csv_contains_time_hours_and_metric_columns(tmp_path):
    result = _run_short_simulation()
    path = export_csv(result, tmp_path / "results.csv")
    df = pd.read_csv(path)

    assert "time_hours" in df.columns
    assert "power.generated_kwh" in df.columns
    assert len(df) == len(result.history)