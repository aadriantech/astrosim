# AGENT — Budgeting

**Scope:** Mission-level energy, mass, reliability accounting.  
**Owns:** `budgeting/*.py`  
**Depends on:** ENG, SUB  
**Last verified:** 2026-06-29 · baseline audit

## Purpose

Accumulate per-subsystem outputs each step into mission budgets attached to `SimulationResult`.

## Gotchas

- Energy budget infers kWh from `power_kw` heuristically when `consumed_kwh` absent — review when adding subsystems.

## Verification status

| Claim | Status |
|-------|--------|
| Energy net = generated − consumed | VERIFIED |
| Mass accumulate + net_import | VERIFIED |
| Reliability exp(−Σrisk) | VERIFIED |

## Tests

- `tests/test_energy_budget.py`, `test_mass_budget.py`, `test_reliability_budget.py`