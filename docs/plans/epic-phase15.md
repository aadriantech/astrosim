---
task_id: epic-phase15
task_class: T2
status: complete
epic: phase15
target_version: "1.1.0"
---

# PDD: Phase 15 — Post-1.0 Community & Performance

## Problem

v1.0.0 closed the original roadmap. Post-1.0 gaps: hardcoded `__version__`, suite missing newest scenarios, sequential-only suite/compare, no academic citation file, no CLI version flag.

## Work order

```
15.1 Dynamic package version     (T1)
15.2 Expanded canonical suite    (T1)
15.3 Parallel suite runner       (T2)
15.4 CITATION.cff                (T1)
15.5 CLI --version               (T1)
15.6 Mars closed-loop study      (T1)
15.7 Release v1.1.0              (T2)
```

## Acceptance

1. [ ] `astrosim.__version__` matches `pyproject.toml` via `importlib.metadata`
2. [ ] Suite includes `mars_closed_loop`, `orbital_greenhouse`
3. [ ] `run_scenario_suite(..., parallel=True)` faster than sequential on 7 scenarios
4. [ ] `CITATION.cff` present at repo root
5. [ ] `astrosim --version` prints version
6. [ ] `docs/studies/mars_closed_loop_study.md` reproducible
7. [ ] ≥168 tests; CI green; tag v1.1.0

## Out of scope

- Live PyPI (still needs token)
- CO₂ chemistry model