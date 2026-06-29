# Changelog

All notable changes to AstroSim are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `scenarios/mars_habitat.json` with full YAML parity
- Active `dust_storm` and `crew_rotation` event handlers
- `tests/test_visualization.py` for matplotlib dashboard PNG output
- Phase 5 contract/export CI gates and registry cleanup (see TASKS.md)

### Changed

- Removed unused `scipy` dependency
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