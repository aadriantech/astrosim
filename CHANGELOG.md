# Changelog

All notable changes to AstroSim are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-06-29

### Added (Phase 15)

- Dynamic `__version__` from package metadata (matches `pyproject.toml`)
- CLI `--version` flag
- Parallel scenario suite (`run_scenario_suite(..., parallel=True)`)
- Expanded canonical suite (8 scenarios incl. mars_closed_loop, orbital_greenhouse)
- `CITATION.cff` for academic citation
- `docs/studies/mars_closed_loop_study.md`

## [1.0.0] - 2026-06-29

### Added (Phase 14)

- `docs/ROADMAP.md` — project completion marker
- All phases 1–14 tracked ✅ in TASKS.md

### Added (Phase 13)

- ISRU–ECLSS O₂ loop (`o2_supplied_kg`, `o2_net_import_kg`)
- `orbital_greenhouse` scenario
- `tests/test_closed_loop_audit.py`

### Added (Phase 12)

- `scripts/verify_pypi_ready.sh` + CI step
- GitHub Pages docs workflow (`.github/workflows/docs.yml`)
- Example study `docs/studies/lunar_energy_trade.md`
- `publish.yml` graceful skip without `PYPI_API_TOKEN`

### Changed

- `__version__` synced to `1.0.0`

## [0.7.0] - 2026-06-29

### Added (Phase 11)

- ISRU–ECLSS water loop (`water_supplied_kg`, reduced `water_net_kg`)
- Structured insight export (`ai/insights.py`) + CLI `--insights-json`
- MC-enhanced compare (`--compare-mc N`)
- NL editor ISRU intents (regolith throughput, isru power)
- `mars_closed_loop` scenario + `examples/run_mars_closed_loop.py`

## [0.6.0] - 2026-06-29

### Added (Phase 10)

- MkDocs site (`mkdocs.yml`, `scripts/build_docs.sh`, `[docs]` extra)
- Dashboard v2: food-loop charts + study report embed
- Scenario suite runner (`analysis/suite.py`) + CLI `--suite`
- `greenhouse_mars` scenario
- CI wheel build smoke (`scripts/smoke_wheel.sh`)
- Contract: `suite_report.schema.json`

## [0.5.0] - 2026-06-29

### Added

- Built-in `GreenhouseSubsystem` with `food_supplied_kg` metric
- ECLSS–greenhouse food loop (`food_net_import_kg`)
- `scenarios/greenhouse_lunar.yaml` + JSON parity
- Study report export (`export/study_report.py`) + CLI `--report`
- Scenario compare API (`analysis/compare.py`) + CLI `--compare`
- NL scenario editor write-back (`--ask --write`, `--force`, `--output`)
- Contracts: `study_report.schema.json`, `scenario_compare.schema.json`
- Examples: `run_greenhouse_lunar.py`, `run_compare.py`

### Changed

- `examples/custom_subsystem.py` uses built-in greenhouse + ephemeral `demo_beacon` plugin
- Mass budget uses `food_net_import_kg` when reported by ECLSS
- PyPI publish documented in `docs/RELEASE.md` (requires `PYPI_API_TOKEN`)

## [0.4.0] - 2026-06-28

### Added

- Monte Carlo envelope option on `run_trade_study()` (`monte_carlo_runs` parameter)
- CI badge in README

### Fixed

- `pyproject.toml` metadata (classifiers/deps were under `[project.urls]`, broke CI install)
- Git remote uses SSH (`github.com-aadriantech` host alias)

### Changed

- Phase 8: trade study CLI, extended NL editor, workflows restored via SSH push

## [0.3.0] - 2026-06-28

### Added

- Pareto trade study API (`analysis/pareto.py`) + CSV export
- NL scenario editor (`ai/scenario_editor.py`) + CLI `--ask` dry-run
- `deep_space_transit` scenario (YAML + JSON)
- ISRU power-limited throughput + `regolith_quality` parameter
- `examples/tutorial.ipynb`, `docs/STUDY_TEMPLATE.md`

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