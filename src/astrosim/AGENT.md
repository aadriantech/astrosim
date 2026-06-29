# AGENT — Package Surface

**Scope:** Public entrypoints, scenario loading, CLI.  
**Owns:** `__init__.py`, `scenario.py`, `cli.py`  
**Depends on:** ENG, SUB, SCE  
**Last verified:** 2026-06-29 · baseline audit

## Purpose

Top-level API: load scenarios, build simulators, run CLI. Re-exports live in subpackages.

## Key entrypoints

- `load_scenario(path)` → `SimulationConfig`
- `build_simulator(config)` → `Simulator`
- `load_and_build(path)` → `Simulator`
- `astrosim` CLI via `cli:main`

## Gotchas

- `build_simulator` creates **fresh subsystem instances** each call (MC reproducibility).
- CLI is subprocess-tested; coverage tool reports 0% on `cli.py` — expected.

## Verification status

| Claim | Status |
|-------|--------|
| YAML + JSON scenario load | VERIFIED |
| CLI smoke + monte-carlo flags | VERIFIED |

## Tests

- `tests/test_scenario.py`, `tests/test_cli.py`

## Related

- [engine/AGENT.md](engine/AGENT.md) · [scenarios/AGENT.md](../../scenarios/AGENT.md)