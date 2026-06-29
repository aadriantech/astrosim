# AGENT — Tests

**Scope:** pytest suite, TDD discipline, coverage gates.  
**Owns:** `tests/*.py`  
**Depends on:** ROOT, TST loads with every code change  
**Last verified:** 2026-06-28 · 71 tests green, 82% cov

## Conventions

- Run: `PYTHONPATH=src pytest tests/ -q`
- Coverage: `pytest --cov=astrosim --cov-report=term-missing` (target ≥80%)
- One concern per test; name describes behavior
- No live network/LLM in CI
- Fix `src/` not tests when requirement is stable

## Layout

| Pattern | Domain |
|---------|--------|
| `test_<subsystem>.py` | Unit |
| `test_simulator.py`, `test_monte_carlo.py` | Engine |
| `test_cli.py` | Subprocess CLI |
| `test_contracts_*.py` | CDD schema, outputs, events, parity |
| `test_srd_features.py` | Cross-cutting integration |

## Do not

- Register permanent fake subsystems without fixture cleanup