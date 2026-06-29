---
task_id: epic-phase7
task_class: T3
status: complete
epic: phase7
srd_refs: ["§2.3", "§2.4"]
prd_refs: ["§4", "§7"]
approver: grok-architect
target_version: "0.3.0"
---

# PDD: Phase 7 — Advanced Analysis & AI-Native Workflows

## Problem

Phase 6 shipped v0.2.0 with timed events, optimization, orbital scenario, and integrity gates. PRD vision still lacks multi-objective trade studies, NL scenario editing, deep-space scenarios, and published community adoption.

## Preconditions

- `bash scripts/integrity_check.sh` green (Phase 6 exit gate)
- `v0.2.0` tagged on GitHub

## Work order

```
7.1 Multi-objective trade studies (T2)
7.2 Deep-space & transit scenarios (T2)
7.3 NL scenario assistant (T2) — LLM parses edit intents
7.4 ISRU model enrichment (T1)
7.5 Docs site & notebooks (T2)
7.6 Community launch (T3) — v0.3.0, study template
```

## Sub-epic 7.1 — Multi-objective trade studies

- `analysis/pareto.py` — sweep two parameters, export CSV of Pareto frontier
- `contracts/trade_study.schema.json`
- Acceptance: lunar solar_kw vs battery_kwh frontier with ≥10 points

## Sub-epic 7.2 — Deep-space scenarios

- `scenarios/deep_space_transit.yaml` + JSON parity
- Reduced crew, long duration, compute-heavy params
- Example `run_deep_space.py`

## Sub-epic 7.3 — NL scenario assistant

- `ai/scenario_editor.py` — prompt → YAML patch dict (mocked in CI)
- CLI `--ask "increase crew to 8"` dry-run mode
- No live LLM in pytest

## Sub-epic 7.4 — ISRU enrichment

- Throughput tied to power budget; regolith quality parameter
- Update `subsystem_outputs.yaml` if new keys required

## Sub-epic 7.5 — Docs & notebooks

- `examples/tutorial.ipynb` Colab-ready
- Optional MkDocs site from existing `docs/`

## Sub-epic 7.6 — Community launch

- v0.3.0 release, study report template in `docs/STUDY_TEMPLATE.md`
- PyPI publish if not done in 6.7

## Out of scope

- 3D rendering, CFD/FEA, HIL, classified data (PRD non-goals)

## Phase 7 exit criteria

- ≥ 110 tests, ≥ 85% coverage
- Integrity check green
- CDD approve all sub-epics