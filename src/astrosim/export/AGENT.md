# AGENT — Export

**Scope:** Serialize results to JSON, CSV, and study reports.  
**Owns:** `export/*.py`  
**Depends on:** VIS  
**Last verified:** 2026-06-29 · Phase 16 interpretation v2 + validation section

## Verification status

| Claim | Status |
|-------|--------|
| JSON structure with config, budgets, history | VERIFIED |
| CSV has time_hours + metrics | VERIFIED |
| JSON schema contract | VERIFIED — `contracts/export_result.schema.json` |
| Study report markdown + JSON sidecar | VERIFIED — `contracts/study_report.schema.json` |
| Implications, verdict, references, actions | VERIFIED — `interpretation.py` |
| Optional validation block in study report | VERIFIED — `--validate` + `--report` |

## Tests

- `tests/test_export.py`
- `tests/test_study_report.py`
- `tests/test_interpretation.py`, `tests/test_interpretation_v2.py`