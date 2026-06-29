# AGENT — Analysis

**Scope:** Sensitivity sweeps, Pareto trade studies, optional scipy optimization.  
**Owns:** `analysis/*.py`  
**Depends on:** ENG, PKG  
**Last verified:** 2026-06-29 · Phase 8

## Purpose

- `one_at_a_time_sensitivity()` — vary one numeric parameter, measure metric elasticity.
- `run_trade_study()` — sweep two parameters, compute Pareto frontier; optional `monte_carlo_runs` adds per-point std envelope (`metric_a_std`, `metric_b_std`).
- `export_trade_study_csv()` — CSV export for trade study results.
- `minimize_metric()` — scipy-backed optimization (`[optimize]` extra).

## Gotchas

- **scipy** is optional (`[optimize]` extra); core deps exclude it.
- MC trade envelope runs full simulations per grid point — keep `monte_carlo_runs` small in CI.

## Verification status

| Claim | Status |
|-------|--------|
| OAT sweep returns perturbations + elasticity | VERIFIED |
| Trade study Pareto frontier + CSV export | VERIFIED |
| MC envelope std fields on trade study | VERIFIED |

## Tests

- `tests/test_srd_features.py::test_sensitivity_analysis`
- `tests/test_pareto.py`
- `tests/test_optimize.py` (with `[optimize]` extra)
- `examples/run_sensitivity.py`, `examples/run_trade_study.py`