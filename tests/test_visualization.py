"""Tests for matplotlib and HTML visualization."""

from __future__ import annotations

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import DEFAULT_SUBSYSTEMS
from astrosim.visualization.dashboard import plot_dashboard


def _run_short_simulation():
    config = SimulationConfig(
        name="viz-test",
        duration_hours=12,
        timestep_hours=6,
        crew_count=1,
        parameters={"solar_array_kw": 40, "base_load_kw": 10},
    )
    return Simulator(config, DEFAULT_SUBSYSTEMS).run()


def test_plot_dashboard_writes_non_empty_png(tmp_path):
    result = _run_short_simulation()
    path = plot_dashboard(result, tmp_path / "dashboard.png")
    assert path.exists()
    assert path.stat().st_size > 500