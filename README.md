# AstroSim

[![CI](https://github.com/aadriantech/astrosim/actions/workflows/ci.yml/badge.svg)](https://github.com/aadriantech/astrosim/actions/workflows/ci.yml)
[![GitHub](https://img.shields.io/github/v/tag/aadriantech/astrosim?label=version)](https://github.com/aadriantech/astrosim/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-MkDocs-blue)](https://aadriantech.github.io/astrosim/)

Open-source, modular simulation framework for modeling, analyzing, and optimizing sustainable human and robotic presence in space — lunar bases, Mars habitats, orbital stations, and deep-space missions.

**Current release: v1.2.0** (public · MIT)

## Features

- **Modular subsystems**: Power, ECLSS, Thermal, Structure, ISRU, Compute/AI, Greenhouse
- **Time-stepped engine** with Monte Carlo uncertainty analysis
- **Budgeting**: energy, mass, and reliability tracking
- **Interpretation**: implications, verdict, references, and recommended actions in study reports
- **Reference validation**: compare results to NASA BVAD/OCHMO baselines (`--validate`)
- **AI hooks**: LLM integration points for optimization and insights (offline mode included)
- **Visualization & export**: matplotlib plots, HTML web dashboard, JSON/CSV output
- **Plugin system**: register custom subsystems via `@register_subsystem`
- **Analysis**: sensitivity sweeps, trade studies, scenario compare/suite, NL scenario editor
- **Example scenarios**: lunar base, Mars habitat, greenhouse, closed-loop Mars, orbital station

## Quick Start

```bash
# Install from GitHub
pip install git+https://github.com/aadriantech/astrosim.git

# Or clone for development
git clone https://github.com/aadriantech/astrosim.git
cd astrosim
pip install -e ".[dev]"

# Run a scenario
astrosim scenarios/greenhouse_lunar.yaml --report --validate --no-plot
```

```bash
# Python API
python examples/run_lunar_base.py
python examples/run_mars_habitat.py
```

Example output: energy/mass budgets, NASA benchmark **PASS/WARN** table, engineering verdict, and parameter suggestions (e.g. increase solar or water recovery).

## CLI highlights

| Flag | What it does |
|------|----------------|
| `--web` | Interactive HTML dashboard |
| `--report` | `study_report.md` + JSON (implications, verdict, actions) |
| `--validate` | Compare to `reference/benchmarks.yaml`; writes `validation_report.json` |
| `--compare` | Multi-scenario metric table |
| `--suite` | Run canonical scenario suite |
| `--monte-carlo N` | Uncertainty summary |
| `--trade-study` | Solar/battery Pareto grid |

## Documentation

| Doc | Description |
|-----|-------------|
| [IO.md](docs/IO.md) | **Inputs & outputs** — scenarios in, reports/dashboards out |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Engine, subsystems, budgets, events, plugins |
| [SCENARIOS.md](docs/SCENARIOS.md) | YAML/JSON schema, parameters, examples |
| [API.md](docs/API.md) | Public interfaces: `Simulator`, `Subsystem`, `AIHooks` |
| [TUTORIAL.md](docs/TUTORIAL.md) | 15-minute getting started |
| [PLUGIN_COOKBOOK.md](docs/PLUGIN_COOKBOOK.md) | Custom subsystem patterns |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Human contributor guide |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [ROADMAP.md](docs/ROADMAP.md) | Phase completion status (v1.2.0) |
| [Example studies](docs/studies/) | Reproducible lunar/Mars trade reports |
| [AGENTS.md](AGENTS.md) | Agent methodology (PDD→TDD→CDD→AYSU) |

Build static docs: `bash scripts/build_docs.sh`

## Project Layout

```
src/astrosim/
  engine/        # Simulation loop and Monte Carlo runner
  subsystems/    # Pluggable habitat subsystem models
  budgeting/     # Energy, mass, reliability accounting
  validation/    # NASA benchmark checks
  export/        # JSON, CSV, study reports, interpretation
  ai/            # LLM hook interfaces
  analysis/      # Sensitivity, compare, suite, trade studies
  visualization/ # Matplotlib + HTML dashboards
reference/       # Official benchmark values (BVAD/OCHMO/ISS)
scenarios/       # YAML scenario definitions
examples/        # Runnable demo scripts
docs/            # Architecture, API, scenarios, contributing
```

## Agent workflow (how this was built)

AstroSim was built with **PDD → TDD → CDD → AYSU** — open-sourced as [ai-coding-scaffold](https://github.com/aadriantech/ai-coding-scaffold).

**Share / promote:** [copy-paste posts for X, Reddit, HN](https://github.com/aadriantech/ai-coding-scaffold/blob/main/docs/SHARE.md)

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

```bash
pip install -e ".[dev]"
pytest
```

## Citation

See [CITATION.cff](CITATION.cff) for academic use.

## License

MIT