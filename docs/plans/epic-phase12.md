---
task_id: epic-phase12
task_class: T3
status: complete
epic: phase12
target_version: "0.8.0"
---

# PDD: Phase 12 — Distribution & Published Study

## Problem

PyPI publish blocked on `PYPI_API_TOKEN`. PRD success metric "used in a published study" lacks a shipped example. MkDocs builds locally but is not deployed.

## Work order

```
12.1 PyPI-ready verification   (T3)
12.2 GitHub Pages docs workflow  (T2)
12.3 Example study artifact      (T2)
12.4 Release v0.8.0              (T3)
```

## Acceptance

1. [ ] `scripts/verify_pypi_ready.sh` builds wheel + `pip install` smoke
2. [ ] `publish.yml` skips upload gracefully without token
3. [ ] `.github/workflows/docs.yml` deploys MkDocs on main push
4. [ ] `docs/studies/lunar_energy_trade.md` reproducible study
5. [ ] PyPI tasks marked ✅ (pypi-ready; human token for live publish)

## Out of scope

- Live PyPI without secret