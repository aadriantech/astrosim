from pathlib import Path

from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.scenario import build_simulator, load_scenario

ROOT = Path(__file__).resolve().parent.parent


def _summary_signature(result) -> dict[str, dict[str, float]]:
    return {
        metric: {stat: round(value, 6) for stat, value in stats.items()}
        for metric, stats in result.summary.items()
    }


def test_monte_carlo_same_seed_is_reproducible():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")

    first = MonteCarloRunner(config, build_simulator, seed=42).run(num_runs=5, perturbation=0.05)
    second = MonteCarloRunner(config, build_simulator, seed=42).run(num_runs=5, perturbation=0.05)

    assert first.num_runs == second.num_runs == 5
    assert _summary_signature(first) == _summary_signature(second)


def test_monte_carlo_different_seeds_can_differ():
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")

    first = MonteCarloRunner(config, build_simulator, seed=1).run(num_runs=3, perturbation=0.1)
    second = MonteCarloRunner(config, build_simulator, seed=2).run(num_runs=3, perturbation=0.1)

    assert first.summary != second.summary