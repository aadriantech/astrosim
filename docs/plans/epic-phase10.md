---
task_id: epic-phase10
task_class: T3
status: complete
epic: phase10
srd_refs: ["§2.4", "§3"]
prd_refs: ["§4", "§7"]
approver: grok-architect
target_version: "0.6.0"
---

# PDD: Phase 10 — Docs Site & Interactive Dashboard

## Problem

Phase 9 delivered biosphere closure and research exports, but community onboarding still relies on scattered markdown files. PyPI remains unpublished (token). The HTML dashboard lacks greenhouse/study-report context deferred from Phase 9. No single command validates all canonical scenarios.

## Preconditions

- Phase 9 exit gate green (`v0.5.0` tagged, CI green)
- `bash scripts/integrity_check.sh` passes

## Work order

```
10.1 PyPI build gate in CI     (T2) — wheel build smoke; carry PyPI publish
10.2 MkDocs static site        (T2) — mkdocs.yml + build script
10.3 Dashboard v2              (T2) — greenhouse + study report embed
10.4 Scenario suite runner     (T2) — run canonical scenarios, suite JSON
10.5 greenhouse_mars scenario  (T1)
10.6 Release v0.6.0            (T3)
```

## 10.1 PyPI build gate

- CI step: `python -m build` succeeds
- `RELEASE.md` unchanged from Phase 9; publish still needs `PYPI_API_TOKEN`

### Acceptance

1. [ ] CI builds wheel/sdist without error
2. [ ] `pip install dist/*.whl` works in clean venv smoke script

## 10.2 MkDocs site

- `mkdocs.yml` at repo root
- `[docs]` optional extra: `mkdocs`, `mkdocs-material`
- `scripts/build_docs.sh` — `mkdocs build -d site/`
- Nav: Tutorial, Architecture, Scenarios, API, Contributing

### Acceptance

1. [ ] `bash scripts/build_docs.sh` exits 0
2. [ ] `site/index.html` exists
3. [ ] README links to docs build instructions

## 10.3 Dashboard v2

- `render_web_dashboard(..., study_report_path=None)` optional sidecar
- Chart series: `greenhouse.food_supplied_kg`, `eclss.food_net_import_kg`
- Study report JSON → reproducibility card in HTML

### Acceptance

1. [ ] `greenhouse_lunar` dashboard includes food metrics when present
2. [ ] Passing `study_report.json` renders reproducibility section
3. [ ] `tests/test_visualization.py` covers new paths

## 10.4 Scenario suite runner

- `analysis/suite.py`: `run_scenario_suite(paths) -> SuiteResult`
- `contracts/suite_report.schema.json`
- `examples/run_suite.py` + CLI `astrosim --suite`

### Acceptance

1. [ ] Suite runs ≥5 canonical scenarios without error
2. [ ] JSON export validates against `suite_report.schema.json`
3. [ ] Completes in < 60s locally

## 10.5 greenhouse_mars

- `scenarios/greenhouse_mars.yaml` + JSON parity
- Subsystems: power, greenhouse, eclss, isru, thermal

## 10.6 Release v0.6.0

- Version bump, CHANGELOG, tag, AGENT sync

## Out of scope

- ReadTheDocs hosting automation
- 3D, CFD, HIL

## Phase 10 exit gate

| # | Criterion |
|---|-----------|
| E1 | ≥155 tests; coverage ≥ 85% |
| E2 | `v0.6.0` tagged; CI green |
| E3 | MkDocs build script green |