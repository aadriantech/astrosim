# AGENT — Export

**Scope:** Serialize results to JSON, CSV, and study reports.  
**Owns:** `export/*.py`  
**Depends on:** VIS  
**Last verified:** 2026-06-29 · Phase 9 study report

## Verification status

| Claim | Status |
|-------|--------|
| JSON structure with config, budgets, history | VERIFIED |
| CSV has time_hours + metrics | VERIFIED |
| JSON schema contract | VERIFIED — `contracts/export_result.schema.json` |
| Study report markdown + JSON sidecar | VERIFIED — `contracts/study_report.schema.json` |

## Tests

- `tests/test_export.py`
- `tests/test_study_report.py`