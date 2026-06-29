---
task_id: epic-phase11
task_class: T3
status: complete
epic: phase11
srd_refs: ["§2.2", "§2.3"]
prd_refs: ["§4", "§7"]
approver: grok-architect
target_version: "0.7.0"
---

# PDD: Phase 11 — Closed-Loop Resources & AI Export

## Problem

Phase 10 improves docs and dashboards but resource loops remain partial: ISRU water does not credit ECLSS, LLM insights lack structured export despite `llm_insight.schema.json`, and compare API lacks Monte Carlo envelopes for uncertainty-aware studies.

## Preconditions

- Phase 10 exit gate green (`v0.6.0` tagged)

## Work order

```
11.1 ISRU–ECLSS water loop     (T2)
11.2 Structured insight export (T2) — llm_insight.schema.json
11.3 MC-enhanced compare       (T2)
11.4 NL editor ISRU intents    (T1)
11.5 mars_closed_loop scenario (T2)
11.6 Release v0.7.0            (T3)
```

## 11.1 ISRU–ECLSS water loop

- ECLSS reads `isru.water_produced_kg` from `state.metrics` (prior step / same-step order)
- New eclss key: `water_supplied_kg`; `water_net_kg` = net import after recovery + ISRU credit
- Mass budget uses updated `water_net_kg`

### Acceptance

1. [ ] Scenario with ISRU shows lower `eclss.water_net_kg` than without
2. [ ] Contract test passes new eclss key
3. [ ] `tests/test_isru_eclss_water_loop.py` green

## 11.2 Structured insight export

- `ai/insights.py`: `export_insight_json(result, path) -> Path`
- CLI `--insights-json` writes validated sidecar
- Mocked adapter path returns `offline: false` when client injected

### Acceptance

1. [ ] Output validates `llm_insight.schema.json`
2. [ ] CLI integration test green
3. [ ] No live LLM in pytest

## 11.3 MC-enhanced compare

- `compare_scenarios(..., monte_carlo_runs: int | None = None)`
- When set, adds `{metric}_mean` and `{metric}_std` from MC summary per scenario
- `contracts/scenario_compare.schema.json` updated for optional std/mean fields

### Acceptance

1. [ ] `monte_carlo_runs=3` adds mean columns for budget metrics
2. [ ] Completes < 30s for 2 scenarios in CI test (short duration override)

## 11.4 NL editor ISRU intents

- Parse `regolith throughput to N` and `set isru power to N kw`
- Tests in `test_scenario_editor.py`

## 11.5 mars_closed_loop scenario

- `scenarios/mars_closed_loop.yaml` + JSON: power, greenhouse, eclss, isru, thermal, structure
- `examples/run_mars_closed_loop.py`

## 11.6 Release v0.7.0

- Version bump, CHANGELOG, tag, AGENT sync

## Out of scope

- Live LLM in CI
- Multiprocessing MC farm

## Phase 11 exit gate

| # | Criterion |
|---|-----------|
| E1 | ≥170 tests; coverage ≥ 85% |
| E2 | `v0.7.0` tagged; CI green |
| E3 | `mars_closed_loop` in parity suite |