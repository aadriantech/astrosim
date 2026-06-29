"""Tests for matplotlib and HTML visualization."""

from __future__ import annotations

from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import DEFAULT_SUBSYSTEMS
from astrosim.scenario import load_and_build
from astrosim.visualization.dashboard import plot_dashboard
from astrosim.visualization.web import render_web_dashboard

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent


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


def test_web_dashboard_includes_food_loop_chart(tmp_path):
    result = load_and_build(ROOT / "scenarios" / "greenhouse_lunar.yaml").run()
    path = render_web_dashboard(result, tmp_path / "dashboard.html")
    html = path.read_text()
    assert "food-chart" in html
    assert "greenhouse_food_supplied" in html


def test_web_dashboard_embeds_study_report(tmp_path):
    result = _run_short_simulation()
    sidecar = tmp_path / "study_report.json"
    sidecar.write_text(
        '{"title":"T","reproducibility_command":"astrosim demo.yaml","method":"deterministic"}'
    )
    path = render_web_dashboard(
        result,
        tmp_path / "dashboard.html",
        study_report_path=sidecar,
    )
    assert "Study Report" in path.read_text()
    assert "astrosim demo.yaml" in path.read_text()