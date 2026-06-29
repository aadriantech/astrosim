# AstroSim

[![CI](https://github.com/aadriantech/astrosim/actions/workflows/ci.yml/badge.svg)](https://github.com/aadriantech/astrosim/actions/workflows/ci.yml)
[![GitHub](https://img.shields.io/github/v/tag/aadriantech/astrosim?label=version)](https://github.com/aadriantech/astrosim/releases)
[![Docs](https://img.shields.io/badge/docs-MkDocs-blue)](https://github.com/aadriantech/astrosim#documentation)

Open-source, modular, AI-native simulation framework for modeling, analyzing, and optimizing sustainable human and robotic presence in space.

## Features (MVP)

- **Modular subsystems**: Power, ECLSS, Thermal, Structure, ISRU, Compute/AI
- **Time-stepped engine** with Monte Carlo uncertainty analysis
- **Budgeting**: energy, mass, and reliability tracking
- **AI hooks**: LLM integration points for optimization and insights
- **Visualization & export**: matplotlib plots, HTML web dashboard, JSON/CSV output
- **Plugin system**: register custom subsystems via `@register_subsystem`
- **Sensitivity analysis**: one-at-a-time parameter sweeps
- **Example scenarios**: lunar base, Mars habitat, greenhouse & closed-loop Mars
- **Research tools**: study reports, scenario compare/suite, trade studies

## Quick Start

```bash
pip install -e ".[dev]"
python examples/run_lunar_base.py
python examples/run_mars_habitat.py
astrosim scenarios/lunar_base.yaml --web
```

## Documentation

| Doc | Description |
|-----|-------------|
| [IO.md](docs/IO.md) | **Inputs & outputs** — scenarios in, JSON/CSV/dashboards out |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Engine, subsystems, budgets, events, plugins |
| [SCENARIOS.md](docs/SCENARIOS.md) | YAML/JSON schema, parameters, examples |
| [API.md](docs/API.md) | Public interfaces: `Simulator`, `Subsystem`, `AIHooks` |
| [AGENTS.md](AGENTS.md) | Agent methodology (PDD→TDD→CDD→AYSU) |
| [AGENT_INDEX.md](AGENT_INDEX.md) | Distributed memory index |
| [TUTORIAL.md](docs/TUTORIAL.md) | 15-minute getting started |
| [PLUGIN_COOKBOOK.md](docs/PLUGIN_COOKBOOK.md) | Custom subsystem patterns |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Human contributor guide |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [MkDocs site](docs/index.md) | Build static docs: `bash scripts/build_docs.sh` |
| [ROADMAP.md](docs/ROADMAP.md) | Phase completion status (v1.0.0) |
| [Example study](docs/studies/lunar_energy_trade.md) | Reproducible lunar energy trade report |
| [PRD.md](docs/PRD.md) | Product requirements |
| [SRD.md](docs/SRD.md) | System requirements |

## Examples

```bash
python examples/run_lunar_base.py
python examples/run_mars_habitat.py
python examples/custom_subsystem.py   # @register_subsystem demo
```

## Project Layout

```
src/astrosim/
  engine/        # Simulation loop and Monte Carlo runner
  subsystems/    # Pluggable habitat subsystem models
  budgeting/     # Energy, mass, reliability accounting
  ai/            # LLM hook interfaces
  analysis/      # Sensitivity analysis
  visualization/ # Matplotlib + HTML dashboards
  export/        # Result serialization
scenarios/       # YAML scenario definitions
examples/        # Runnable demo scripts
docs/            # Architecture, API, scenarios, contributing
```

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md). Run tests with:

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT