# AGENT — Visualization

**Scope:** Matplotlib PNG + self-contained HTML dashboard.  
**Owns:** `visualization/*.py`  
**Depends on:** ENG  
**Last verified:** 2026-06-29 · Phase 10 dashboard v2

## Gotchas

- Matplotlib dashboard is 2×3 grid; PNG path tested in `tests/test_visualization.py`.

## Verification status

| Claim | Status |
|-------|--------|
| HTML dashboard renders scenario name | VERIFIED |
| Food-loop charts when greenhouse present | VERIFIED |
| Study report sidecar embed | VERIFIED |
| Web ECLSS + thermal series | VERIFIED |
| Matplotlib PNG export | VERIFIED |

## Tests

- `tests/test_visualization.py`, `tests/test_srd_features.py::test_web_dashboard_generation`