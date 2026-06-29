# AGENT — Export

**Scope:** Serialize results to JSON and CSV.  
**Owns:** `export/*.py`  
**Depends on:** VIS  
**Last verified:** 2026-06-29 · baseline audit

## Verification status

| Claim | Status |
|-------|--------|
| JSON structure with config, budgets, history | VERIFIED |
| CSV has time_hours + metrics | VERIFIED |
| JSON schema contract | VERIFIED — `contracts/export_result.schema.json` |

## Tests

- `tests/test_export.py`