# AGENT — Analysis

**Scope:** Sensitivity sweeps (not scipy.optimize yet).  
**Owns:** `analysis/*.py`  
**Depends on:** ENG, PKG  
**Last verified:** 2026-06-29 · baseline audit

## Purpose

`one_at_a_time_sensitivity()` varies one numeric parameter and measures metric elasticity.

## Gotchas

- **scipy** removed from deps (unused); future optimization epic may re-add.

## Verification status

| Claim | Status |
|-------|--------|
| OAT sweep returns perturbations + elasticity | VERIFIED |

## Tests

- `tests/test_srd_features.py::test_sensitivity_analysis`
- `examples/run_sensitivity.py`