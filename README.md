# AstroSim

Open-source, modular, AI-native simulation framework for modeling, analyzing, and optimizing sustainable human and robotic presence in space.

## Features (MVP)

- **Modular subsystems**: Power, ECLSS, Thermal, Structure, ISRU, Compute/AI
- **Time-stepped engine** with Monte Carlo uncertainty analysis
- **Budgeting**: energy, mass, and reliability tracking
- **AI hooks**: LLM integration points for optimization and insights
- **Visualization & export**: matplotlib plots, HTML web dashboard, JSON/CSV output
- **Plugin system**: register custom subsystems via `@register_subsystem`
- **Sensitivity analysis**: one-at-a-time parameter sweeps
- **Example scenarios**: lunar base and Mars habitat

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
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Engine, subsystems, budgets, events, plugins |
| [SCENARIOS.md](docs/SCENARIOS.md) | YAML/JSON schema, parameters, examples |
| [API.md](docs/API.md) | Public interfaces: `Simulator`, `Subsystem`, `AIHooks` |
| [AGENTS.md](AGENTS.md) | Agent methodology (PDD→TDD→CDD→AYSU) |
| [AGENT_INDEX.md](AGENT_INDEX.md) | Distributed memory index |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Human contributor guide |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
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