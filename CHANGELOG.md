# Changelog

All notable changes to AstroSim are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-28

### Added

- Timed event recovery (`duration_hours`) for `dust_storm` and `crew_rotation`
- `minimize_metric()` optimization API with `[optimize]` optional extra
- `scenarios/orbital_station.yaml` + JSON parity
- `scripts/integrity_check.sh` system integrity gate
- `scripts/benchmark_sim.py`, `smoke_mars_quick.sh`, `smoke_llm.sh`
- `tests/test_ai_adapters.py`, `tests/test_optimize.py`, `tests/test_cli_unit.py`
- `docs/TUTORIAL.md`, `docs/PLUGIN_COOKBOOK.md`, `docs/RELEASE.md`, `docs/PERFORMANCE.md`
- PyPI publish workflow (manual dispatch)

### Changed

- CLI helpers extracted for unit testing
- `custom_subsystem.py` unregisters plugin on exit
- CI installs `[dev,optimize]` and runs extended smokes

## [0.1.1] - 2026-06-28

### Added

- `scenarios/mars_habitat.json` with full YAML parity
- Active `dust_storm` and `crew_rotation` event handlers
- `tests/test_visualization.py` for matplotlib dashboard PNG output
- Phase 5 contract/export CI gates and registry cleanup

### Changed

- Removed unused `scipy` from core dependencies
- Parity tests parametrized for lunar and Mars scenarios

## [0.1.0] - 2026-06-28

### Added

- **Core simulation engine** — `Simulator` with discrete time-stepping, state history, and event queue
- **Subsystem framework** — abstract `Subsystem` base class and `@register_subsystem` plugin registry
- **Built-in subsystems** — Power, ECLSS, Thermal, Structure, ISRU, and Compute/AI models
- **Budgeting** — energy, mass, and reliability trackers with per-subsystem accumulation
- **Scenario loading** — YAML and JSON support via `load_scenario` and `load_and_build`
- **Monte Carlo analysis** — parameter perturbation with statistical summaries
- **Sensitivity analysis** — one-at-a-time parameter sweeps with elasticity
- **AI hooks** — `AIHooks` for offline insights and LLM integration via `LLMClient` protocol
- **Visualization** — matplotlib dashboard and standalone HTML web dashboard
- **Export** — JSON and CSV result serialization
- **CLI** — `astrosim` command with `--web` and `--output-dir` options
- **Example scenarios** — lunar base and Mars habitat definitions
- **Example scripts** — `run_lunar_base.py` and `run_mars_habitat.py`
- **Test suite** — unit tests for engine, subsystems, budgets, and scenario loading
- **Documentation** — PRD, SRD, architecture, API, scenarios, and contributing guides

### Notes

- MVP release targeting research and education use
- Python 3.10+ required; tested on 3.11 in CI
- MIT licensed

[0.1.0]: https://github.com/aadriantech/astrosim/releases/tag/v0.1.0