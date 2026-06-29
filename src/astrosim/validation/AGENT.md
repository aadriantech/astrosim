# AGENT — Validation

**Scope:** Compare simulation results to official/public reference benchmarks.  
**Owns:** `validation/*.py`, `reference/benchmarks.yaml`  
**Depends on:** ENG, SCE  
**Last verified:** 2026-06-29 · Phase 16

## Purpose

Provide traceable accuracy checks: parameter fidelity vs BVAD/OCHMO, derived ECLSS rate sanity,
and soft scenario envelopes (e.g. `orbital_station`).

## Gotchas

- Parameter fidelity **warns** (not fails) when scenarios intentionally differ from BVAD defaults.
- Envelope energy band is wide — simplified power model over-surplus vs ISS.
- Call `validate_result(..., scenario_path=...)` for envelope matching by file name.

## Verification status

| Claim | Status |
|-------|--------|
| Load `reference/benchmarks.yaml` | VERIFIED |
| Parameter + derived + envelope checks | VERIFIED |
| `validation_report.schema.json` contract | VERIFIED |
| CLI `--validate` writes JSON + table | VERIFIED |

## Tests

- `tests/test_reference_validation.py`
- `tests/test_contracts_validation.py`
- `tests/test_cli.py::test_cli_validate_writes_report`