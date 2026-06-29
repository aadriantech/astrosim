# Contributing to AstroSim

Development follows **PDD → TDD → CDD → AYSU**. Read [AGENTS.md](../AGENTS.md) and [AGENT_INDEX.md](../AGENT_INDEX.md) before coding.

## Prerequisites

```bash
git clone https://github.com/aadriantech/astrosim.git
cd astrosim
pip install -e ".[dev]"
```

## Workflow

| Step | Skill | Output |
|------|-------|--------|
| **PDD** | `/pdd-plan` | `docs/plans/<epic>.md` |
| **TDD** | `/tdd-implement` | failing tests → green `src/` |
| **CDD** | `/cdd-review` | `reviews/<task-id>.md` |
| **AYSU** | `/aysu-verify` | structured verification block |

### Task classes

| Class | Pipeline |
|-------|----------|
| T0 typo/docs | TDD → AYSU |
| T1 single module | Light PDD → TDD → AYSU |
| T2 cross-module | Full PDD → TDD → CDD → AYSU |
| T3 release/infra | Full + human sign-off |

## Memory protocol

1. Read `AGENT_INDEX.md`
2. Load **one** primary section `AGENT.md` (+ up to 2 secondary)
3. After behavior changes: `/memory-sync`

Section template: [AGENT_TEMPLATE.md](AGENT_TEMPLATE.md)

## Tests

```bash
pytest
PYTHONPATH=src pytest tests/ -q
pytest --cov=astrosim --cov-report=term-missing
bash scripts/check_agent_sync.sh
```

## Pull requests

Use the PR template. T2+ requires critic `recommendation: approve`.

## SRD → test mapping

See [CONTRIBUTING SRD table](#srd-requirements--test-mapping) below (unchanged).

## Related

- [API.md](API.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [SCENARIOS.md](SCENARIOS.md)
- Skills: `.grok/skills/pdd-plan`, `tdd-implement`, `cdd-review`, `aysu-verify`, `memory-sync`

---

## SRD Requirements → Test Mapping

| SRD § | Requirement | Test module / function |
|-------|-------------|------------------------|
| 2.1 | Discrete time-step simulation | `tests/test_simulator.py::test_simulator_runs_all_steps` |
| 2.1 | State history recording | `tests/test_simulator.py::test_final_state_is_last_history_entry` |
| 2.1 | Event-driven updates | `tests/test_srd_features.py::test_event_driven_updates` |
| 2.1 | Monte Carlo / stochastic | `tests/test_monte_carlo.py` |
| 2.2 | Subsystem plugin registry | `tests/test_subsystem_base.py`, `tests/test_srd_features.py::test_plugin_registry_lists_builtins` |
| 2.2 | Power subsystem | `tests/test_power.py` |
| 2.2 | ECLSS subsystem | `tests/test_eclss.py` |
| 2.2 | Thermal subsystem | `tests/test_thermal.py` |
| 2.2 | ISRU subsystem | `tests/test_isru.py` |
| 2.2 | Compute subsystem | `tests/test_compute.py` |
| 2.2 | Structure / risk | `tests/test_structure.py` |
| 2.3 | Energy budget | `tests/test_energy_budget.py` |
| 2.3 | Mass budget | `tests/test_mass_budget.py` |
| 2.3 | Reliability budget | `tests/test_reliability_budget.py` |
| 2.3 | Sensitivity analysis | `tests/test_srd_features.py::test_sensitivity_analysis` |
| 2.3 | AI / optimization hooks | `tests/test_ai_hooks.py` |
| 2.4 | Scenario YAML/JSON loading | `tests/test_scenario.py`, `tests/test_contracts_scenario.py` |
| 2.4 | Scenario contracts | `tests/test_contracts_parity.py`, `tests/test_contracts_events.py` |
| 2.4 | Export JSON / CSV | `tests/test_export.py` |
| 2.4 | CLI | `tests/test_cli.py` |
| 2.4 | Web dashboard | `tests/test_srd_features.py::test_web_dashboard_generation` |

## License

MIT — see [LICENSE](../LICENSE).