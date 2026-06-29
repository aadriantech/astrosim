# AGENT — Visualization

**Scope:** Matplotlib PNG + self-contained HTML dashboard.  
**Owns:** `visualization/*.py`  
**Depends on:** ENG  
**Last verified:** 2026-06-29 · baseline audit

## Gotchas

- Matplotlib dashboard is 2×3 grid; low line coverage — PNG path under-tested in CI.

## Verification status

| Claim | Status |
|-------|--------|
| HTML dashboard renders scenario name | VERIFIED |
| Web ECLSS + thermal series | VERIFIED |

## Tests

- `tests/test_srd_features.py::test_web_dashboard_generation`