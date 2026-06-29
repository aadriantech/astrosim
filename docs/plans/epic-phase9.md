---
task_id: epic-phase9
task_class: T3
status: complete
epic: phase9
srd_refs: ["§2.2", "§2.3", "§2.4"]
prd_refs: ["§4", "§7"]
approver: grok-architect
target_version: "0.5.0"
---

# PDD: Phase 9 — Research Workflows & Biosphere Closure

## Problem

Phases 1–8 delivered a production-hardened framework (v0.4.0, CI green, trade studies, NL editor dry-run). PRD success metrics are still partially unmet:

| PRD metric | Gap |
|------------|-----|
| Active GitHub community | Package not on PyPI (`pip install astrosim` fails) |
| Used in a published study | `STUDY_TEMPLATE.md` exists but no automated report export |
| Sustainable habitat modeling | Food is import-only in ECLSS; greenhouse exists only as a plugin demo |

Researchers need **closed-loop biosphere scenarios**, **batch scenario comparison**, and **one-command study artifacts** — without violating non-goals (no 3D, CFD, HIL).

## Preconditions

- Phase 8 exit gate green (`bash scripts/integrity_check.sh`, CI on `main`)
- `v0.4.0` tagged on GitHub
- SSH remote configured (`github.com-aadriantech`)

## Work order (strict)

```
9.1 PyPI distribution          (T3) — unblock pip install; carry over 8.5.1.3
    ↓
9.2 Greenhouse built-in        (T2) — promote plugin demo to core subsystem
    ↓
9.3 ECLSS–greenhouse food loop (T2) — biomass offsets food import
    ↓
9.4 Study report generator     (T2) — markdown export from results
    ↓
9.5 Scenario batch compare     (T2) — multi-scenario metric table
    ↓
9.6 NL editor write-back       (T1) — CLI --ask --write
    ↓
9.7 Release v0.5.0             (T3) — tag, CHANGELOG, example scenario
```

Sub-epics 9.4 and 9.5 may run in parallel after 9.2 completes. Do not start 9.3 before 9.2 greenhouse contract is active.

---

## Architect decisions

| Topic | Decision |
|-------|----------|
| Version target | `0.5.0` at end of Phase 9 |
| PyPI | Manual `workflow_dispatch` via existing `publish.yml`; document TestPyPI fallback in `RELEASE.md` |
| Greenhouse location | `src/astrosim/subsystems/greenhouse.py`; remove duplicate from `examples/custom_subsystem.py` (example imports built-in) |
| Food coupling | ECLSS reads `state.metrics["greenhouse.food_supplied_kg"]` when present; net food import = `food_consumed - food_supplied` |
| Study report format | Markdown only (no PDF); fills `docs/STUDY_TEMPLATE.md` sections from `SimulationResult` + budgets |
| Compare API | `analysis/compare.py` returns list of dicts; CSV export optional; no new subsystem types |
| NL write-back | `--write` flag writes patched YAML beside source (`*.patched.yaml`) unless `--output` given; never overwrites source without `--force` |
| MkDocs site | Out of scope (defer to Phase 10) |

---

## Sub-epic 9.1 — PyPI Distribution (T3)

**Problem:** `8.5.1.3` deferred; README install instructions assume pip but package is GitHub-only.

### Interfaces

- `.github/workflows/publish.yml` (existing) — requires `PYPI_API_TOKEN` secret
- `README.md` — add PyPI badge + `pip install astrosim` once published
- `docs/RELEASE.md` — TestPyPI smoke steps

### Acceptance criteria

1. [ ] `PYPI_API_TOKEN` documented in `RELEASE.md` (human sets GitHub secret)
2. [ ] TestPyPI upload documented OR successful publish to PyPI for `0.5.0`
3. [ ] `pip install astrosim==0.5.0` succeeds in clean venv; `astrosim --help` runs
4. [ ] README shows PyPI install line and version badge

### Out of scope

- Automated publish on every tag (manual dispatch only for now)

---

## Sub-epic 9.2 — Greenhouse Built-in Subsystem (T2)

**Problem:** Biomass model lives in `examples/custom_subsystem.py`; not in contract manifest or default scenarios.

### Interfaces

- `src/astrosim/subsystems/greenhouse.py` — new `GreenhouseSubsystem`
- `contracts/subsystem_outputs.yaml` — add `greenhouse` required keys:
  - `biomass_kg`, `growth_kg`, `food_supplied_kg`, `power_kw`
- `src/astrosim/subsystems/__init__.py` — export and auto-register
- `examples/custom_subsystem.py` — refactor to import built-in; keep `unregister_subsystem` smoke pattern for third-party plugins

### Edge cases

1. Zero crew → growth uses base rate only (no tending bonus)
2. Negative growth rate param → clamp to 0
3. Scenario without `greenhouse` in subsystems list → ECLSS unaffected (9.3)

### Acceptance criteria

1. [ ] `GreenhouseSubsystem` registered as `"greenhouse"` in `build_subsystems(["greenhouse"])`
2. [ ] Contract test in `tests/test_contracts_subsystems.py` validates greenhouse keys
3. [ ] `food_supplied_kg` = `growth_kg × food_yield_fraction` (default fraction 0.8)
4. [ ] `examples/custom_subsystem.py` smoke still passes (uses built-in or isolated plugin)
5. [ ] `subsystem_outputs.yaml` lists greenhouse manifest

### Out of scope

- CO₂ scrubbing from greenhouse (defer)
- Multi-crop species model

---

## Sub-epic 9.3 — ECLSS–Greenhouse Food Loop (T2)

**Problem:** ECLSS always treats food as net import; closed-loop habitats need local production credit.

### Interfaces

- `src/astrosim/subsystems/eclss.py` — read prior-step `greenhouse.food_supplied_kg` from `state.metrics`
- New metric: `food_supplied_kg` (from greenhouse), `food_net_import_kg` (consumed − supplied)
- `contracts/subsystem_outputs.yaml` — add `food_supplied_kg`, `food_net_import_kg` to eclss required keys
- `scenarios/greenhouse_lunar.yaml` + JSON parity — subsystems: `[power, eclss, greenhouse, thermal]`

### Edge cases

1. Greenhouse not in scenario → `food_supplied_kg = 0`, behavior unchanged vs v0.4
2. Supplied exceeds consumed → `food_net_import_kg` clamped to 0; no negative mass credit beyond consumed
3. Mass balance: only `food_net_import_kg` added to `state.mass_kg` (not full consumed)

### Acceptance criteria

1. [ ] Lunar scenario with greenhouse shows lower `food_net_import_kg` than without greenhouse (same params)
2. [ ] `state.mass_kg` delta uses net food import, not gross consumed
3. [ ] Contract test validates new eclss keys
4. [ ] `scenarios/greenhouse_lunar.yaml` + `.json` pass `test_contracts_scenario.py`
5. [ ] `examples/run_greenhouse_lunar.py` exports JSON + dashboard

### Out of scope

- Water recycling from greenhouse transpiration
- Dynamic crew nutrition requirements

---

## Sub-epic 9.4 — Study Report Generator (T2)

**Problem:** `STUDY_TEMPLATE.md` is manual; researchers need reproducible markdown artifacts.

### Interfaces

- `src/astrosim/export/study_report.py` — `render_study_report(result, config, *, output_path, method="deterministic")`
- `contracts/study_report.schema.json` (planned → active) — metadata block: scenario name, duration, metrics table, reproducibility command
- CLI flag: `astrosim <scenario> --report` writes `study_report.md` to output dir
- `examples/run_lunar_base.py` — optionally emit report

### Edge cases

1. Missing budget fields → omit row with "N/A"
2. MC results → `method="monte_carlo"` includes p5/p95 if available
3. Non-UTF8 scenario names → ASCII-fallback in filename

### Acceptance criteria

1. [ ] `render_study_report()` produces markdown with Objective, Scenario, Methods, Key Results table, Reproducibility sections
2. [ ] Key Results includes energy net, mass net import, mission success probability when budgets present
3. [ ] `tests/test_study_report.py` validates output contains scenario name and ≥3 metric rows
4. [ ] `contracts/study_report.schema.json` validates exported metadata JSON sidecar (`study_report.json`)
5. [ ] CLI `--report` integration test in `tests/test_cli.py` or subprocess smoke

### Out of scope

- LaTeX/PDF rendering
- Auto-generated figures embedded in report (link to dashboard path only)

---

## Sub-epic 9.5 — Scenario Batch Compare (T2)

**Problem:** No API to run multiple scenarios and rank/compare outcomes for trade decisions.

### Interfaces

- `src/astrosim/analysis/compare.py`:
  - `compare_scenarios(paths: list[Path], metrics: list[str]) -> CompareResult`
  - `export_compare_csv(result, path) -> Path`
- `contracts/scenario_compare.schema.json` (planned → active)
- CLI: `astrosim --compare scenarios/a.yaml scenarios/b.yaml --metrics power.stored_kwh,eclss.water_net_kg`
- `examples/run_compare.py` — lunar vs mars vs orbital snapshot

### Edge cases

1. Scenario load failure → skip with warning in result.errors list
2. Missing metric in a run → `null` in table
3. Different subsystem sets → compare only requested metrics that exist

### Acceptance criteria

1. [ ] `compare_scenarios()` runs ≥2 scenarios and returns aligned metric columns
2. [ ] CSV export has header row scenario_name + requested metrics
3. [ ] Schema validation test for `scenario_compare.schema.json`
4. [ ] CLI `--compare` prints table to stdout and optional `--output-dir`
5. [ ] `examples/run_compare.py` completes in integrity check smoke (< 30s total)

### Out of scope

- Statistical significance testing across MC ensembles
- Parallel multiprocessing (sequential runs OK for v0.5)

---

## Sub-epic 9.6 — NL Editor Write-back (T1)

**Problem:** `--ask` dry-run only; users cannot persist edits without manual YAML editing.

### Interfaces

- `src/astrosim/cli.py` — add `--write` and `--force` flags to `--ask` flow
- Output default: `<stem>.patched.yaml` adjacent to source

### Acceptance criteria

1. [ ] `astrosim scenario.yaml --ask "set crew to 6" --write` creates patched file with updated `crew_count`
2. [ ] Without `--force`, existing output file raises clear error (exit code 1)
3. [ ] `--output path.yaml` overrides default patched path
4. [ ] Tests in `tests/test_scenario_editor.py` cover write path (tmp_path)

### Out of scope

- LLM-backed parsing (remain offline heuristic)
- In-place overwrite of source scenario

---

## Sub-epic 9.7 — Release v0.5.0 (T3)

### Acceptance criteria

1. [ ] Version `0.5.0` in `pyproject.toml` and `CHANGELOG.md`
2. [ ] Tag `v0.5.0` pushed via SSH
3. [ ] CI green on release commit
4. [ ] `TASKS.md` Phase 9 all ✅
5. [ ] `AGENT_INDEX.md` synced (subsystems, export, analysis sections)
6. [ ] CDD reviews for 9.2–9.5 with `recommendation: approve`

---

## Phase 9 exit criteria (AYSU gate)

| # | Criterion |
|---|-----------|
| E1 | `v0.5.0` tag on GitHub; PyPI install works OR documented blocker with TestPyPI proof |
| E2 | ≥ 130 tests; coverage ≥ 85% |
| E3 | `greenhouse_lunar` scenario in contract parity suite |
| E4 | Integrity check green |
| E5 | No open critical/high CDD findings on Phase 9 sub-epics |
| E6 | `contracts/README.md` lists `study_report` and `scenario_compare` as active |

---

## Out of scope (Phase 9)

- 3D rendering, CFD/FEA, hardware-in-the-loop (PRD non-goals)
- MkDocs / ReadTheDocs site
- Live LLM in CI
- Multiprocessing scenario farm
- Conference paper / human publication (template supports, not automated)

---

## CDD focus areas

| Sub-epic | Scrutinize |
|----------|------------|
| 9.2–9.3 | Mass balance correctness; backward compat without greenhouse |
| 9.4 | Report must not invent metrics; N/A handling |
| 9.5 | Error aggregation; no silent scenario skip without logging |
| 9.6 | File overwrite safety (`--force` gate) |
| 9.1 | No secrets in repo; token docs only |

---

## Implementation notes

- Register greenhouse in `subsystems/__init__.py` alongside power/eclss imports so default discovery works.
- ECLSS food coupling: use `state.metrics.get("greenhouse.food_supplied_kg", 0.0)` at start of `update()` — metrics reflect **previous** step outputs (existing engine semantics).
- Compare API should reuse `load_scenario` + `build_simulator` from `scenario.py` — no duplicate YAML parsing.
- Study report sidecar JSON enables future web dashboard ingestion (Phase 10).

---

## TASKS.md mapping (for tracker update)

| ID | Task |
|----|------|
| 9.1.1.1 | PyPI token docs + publish |
| 9.2.1.1 | Greenhouse subsystem + contract |
| 9.3.1.1 | ECLSS food loop + greenhouse_lunar scenario |
| 9.4.1.1 | Study report export + CLI `--report` |
| 9.5.1.1 | Scenario compare API + CLI |
| 9.6.1.1 | NL editor `--write` |
| 9.7.1.1 | Release v0.5.0 |