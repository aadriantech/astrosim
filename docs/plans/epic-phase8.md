---
task_id: epic-phase8
task_class: T3
status: ready
epic: phase8
target_version: "0.4.0"
approver: grok-architect
---

# PDD: Phase 8 — CI Restore & Production Hardening

## Problem

Code is local-complete through Phase 7 but GitHub push blocked on `workflow` OAuth scope. Remote may lack CI workflows. Need production-ready repo + extended analysis.

## Work order

```
8.1 Restore CI on GitHub (T3)
8.2 Trade study CLI + examples (T2)
8.3 Extended NL editor patterns (T1)
8.4 Monte Carlo trade uncertainty (T2)
8.5 PyPI publish + README badges (T3)
```

## 8.1 Restore CI

1. [ ] `gh auth refresh -h github.com -s workflow,repo`
2. [ ] Restore `.github/workflows/` and push
3. [ ] Remote Actions green

## 8.2 Trade study CLI

- `astrosim --trade-study` flag
- `examples/run_trade_study.py`

## 8.3 NL editor

- Parse battery_kwh, duration_hours intents
- Tests in `test_scenario_editor.py`

## 8.4 MC + trade

- `run_trade_study` optional MC envelope per grid point

## 8.5 Release 0.4.0

- PyPI publish, CI badge in README

## Out of scope

- 3D, CFD, HIL