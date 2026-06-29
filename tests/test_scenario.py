from pathlib import Path

from astrosim.scenario import load_scenario

ROOT = Path(__file__).resolve().parent.parent


def test_load_lunar_scenario():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    assert config.name == "Lunar Base Alpha"
    assert config.crew_count == 4
    assert config.location == "lunar"
    assert config.num_steps == 120


def test_load_mars_scenario():
    config = load_scenario(ROOT / "scenarios" / "mars_habitat.yaml")
    assert config.name == "Mars Habitat One"
    assert config.crew_count == 6
    assert config.location == "mars"
    assert len(config.events) == 2
    assert config.events[0].name == "dust_storm"
    assert config.events[1].name == "isru_ramp_up"