# AGENT — Simulation Engine

**Scope:** Time-stepped simulation, events, Monte Carlo, state.  
**Owns:** `engine/*.py`  
**Depends on:** SUB, BUD  
**Last verified:** 2026-06-29 · baseline audit

## Purpose

`Simulator.run()` loops discrete timesteps, invokes subsystems, records history and budgets.

## Key concepts

- **SimulationState:** mutable per-step state; snapshotted into history.
- **SimulationConfig:** duration, Δt, parameters, events, subsystem filter.
- **EventQueue:** fires events when `time_hours` matches step time.

## Gotchas

- Simulator calls `subsystem.update()` directly and updates `_local_state` itself — prefer `step()` in unit tests for `get_state()`.
- Event handlers cataloged in `contracts/events.yaml`; all cataloged events are `active`.

## Verification status

| Claim | Status |
|-------|--------|
| Discrete stepping + history | VERIFIED |
| Monte Carlo seed reproducibility | VERIFIED |
| Event handler semantics | VERIFIED — `tests/test_contracts_events.py` |

## Tests

- `tests/test_simulator.py`, `tests/test_monte_carlo.py`, `tests/test_contracts_events.py`

## Related

- Contract: [contracts/events.yaml](../../../contracts/events.yaml)
- Plan: `docs/plans/epic-contracts.md`