"""Integration audit: closed-loop Mars habitat reduces mass imports."""

from pathlib import Path

from astrosim.scenario import load_and_build

ROOT = Path(__file__).resolve().parent.parent


def _run(path: str) -> dict[str, float]:
    result = load_and_build(ROOT / "scenarios" / path).run()
    final = result.final_state
    assert final is not None
    return {
        "food_net": final.metrics.get("eclss.food_net_import_kg", 0.0),
        "water_net": final.metrics.get("eclss.water_net_kg", 0.0),
        "o2_net": final.metrics.get("eclss.o2_net_import_kg", 0.0),
        "mass_import": result.mass_budget.net_import_kg if result.mass_budget else 0.0,
    }


def test_mars_closed_loop_beats_mars_habitat_imports():
    closed = _run("mars_closed_loop.yaml")
    baseline = _run("mars_habitat.yaml")
    assert closed["food_net"] < baseline["food_net"]
    assert closed["water_net"] <= baseline["water_net"]
    assert closed["o2_net"] >= 0.0
    assert closed["mass_import"] < baseline["mass_import"]