---
task_id: epic-phase6
task_class: T3
status: complete
epic: phase6
srd_refs: ["§2.3", "§2.4", "§3"]
prd_refs: ["§4", "§7"]
approver: grok-architect
target_version: "0.2.0"
---

# PDD: Phase 6 — Post-MVP Growth

## Problem

Phases 1–5 delivered a contract-governed MVP (83 tests, 85% coverage, CI gates). The product is not yet **publicly shipped** (GitHub push blocked), analysis is limited to OAT sensitivity, events lack duration/recovery semantics, LLM adapters are untested, and PRD success metrics (community, published use) are unmet.

Phase 6 turns the MVP into a **shippable, extensible v0.2.0** without violating PRD non-goals (no 3D, CFD, HIL, classified data).

## Goals (PRD-aligned)

| Goal | Phase 6 deliverable |
|------|-------------------|
| Active GitHub community | Public repo, tagged release, contributing onboarding |
| Engineering acceleration | Timed events, parameter optimization, trade-study export |
| AI-native framework | Mocked + opt-in live LLM tests; documented adapter usage |
| Education / research | Tutorial notebook, plugin cookbook, reference orbital scenario |

## Work order (strict)

```
6.1 Release & Distribution   (T3) — unblock everything else
    ↓
6.2 Quality & Performance    (T2) — harden before feature expansion
    ↓
6.3 Event Semantics v2       (T2) — timed recovery, contract update
    ↓
6.4 Optimization             (T2) — scipy optional extra
    ↓
6.5 AI Integration Hardening (T2) — mock tests + opt-in smoke
    ↓
6.6 Scenarios & Examples     (T2) — orbital template, example hygiene
    ↓
6.7 Community & Packaging    (T2/T3) — PyPI, tutorial, v0.2.0 tag
```

Sub-epics may run in parallel **after** 6.1 completes. Do not start 6.4 before 6.2 perf baseline exists.

---

## Architect decisions

| Topic | Decision |
|-------|----------|
| Version target | `0.2.0` at end of Phase 6; tag `0.1.0` at 6.1 completion |
| scipy | Re-add as **optional** `[optimize]` extra only — not core dep |
| LLM in CI | Mocked unit tests only; live smoke via `scripts/smoke_llm.sh` (skipped without key) |
| Event duration | Payload `duration_hours` (optional); default permanent for backward compat |
| Dust storm recovery | Restore pre-storm `solar_capacity_factor` when duration elapses |
| PyPI | Publish after 6.1 GitHub release; use `hatchling` existing build |
| Perf gate | Benchmark script, not CI blocker initially — report-only in 6.2 |
| Orbital scenario | New `scenarios/orbital_station.yaml` — lighter than lunar, no new subsystems |
| CLI coverage | Extract testable helpers from `cli.py`; keep subprocess test as integration |
| Plugin pollution | `custom_subsystem.py` uses `unregister_subsystem` on exit or isolated subprocess smoke |

---

## Sub-epic 6.1 — Release & Distribution (T3)

**Problem:** Two local commits; no remote; no release tag.

### Interfaces

- `.github/workflows/release.yml` (planned) — tag push → GitHub Release notes
- `CHANGELOG.md` — move Unreleased → `[0.1.0]`

### Acceptance criteria

1. [ ] `git push origin main` succeeds (human credential step documented in `docs/RELEASE.md`)
2. [ ] Git tag `v0.1.0` created and pushed
3. [ ] `CHANGELOG.md` `[0.1.0]` section complete; Unreleased cleared or reset for 0.2.0
4. [ ] `docs/RELEASE.md` documents push, tag, and CI verification steps
5. [ ] GitHub Actions green on `main` after push

### Out of scope

- PyPI publish (6.7)

---

## Sub-epic 6.2 — Quality & Performance (T2)

**Problem:** `cli.py` 0% unit coverage; no perf baseline; `custom_subsystem.py` pollutes registry.

### Interfaces

- `scripts/benchmark_sim.py` (new) — times 1-year lunar sim, prints wall seconds
- `scripts/smoke_custom_subsystem.sh` (new) — subprocess isolation

### Acceptance criteria

1. [ ] `scripts/benchmark_sim.py` runs lunar scenario (8760h) in < 30s on CI runner (soft assert, warn-only first)
2. [ ] CLI argument parsing extracted to testable functions; unit tests added; coverage on `cli.py` ≥ 60%
3. [ ] `custom_subsystem.py` smoke runs in subprocess OR calls `unregister_subsystem("greenhouse")` on exit
4. [ ] `tests/AGENT.md` documents benchmark + CLI coverage conventions
5. [ ] Full suite + 80% package coverage still green

### Edge cases

1. Benchmark on slow runner — use warn threshold, not hard fail in 6.2
2. Matplotlib headless — `MPLBACKEND=Agg` in benchmark script

---

## Sub-epic 6.3 — Event Semantics v2 (T2)

**Problem:** `dust_storm` permanently reduces solar CF; no duration model; contracts describe instant mutation only.

### Interfaces

- `contracts/events.yaml` — add `duration_hours` semantics for `dust_storm`, `crew_rotation`
- `src/astrosim/engine/events.py` — `apply_event_payload`, new `tick_event_recovery(config, time_hours)`
- `Simulator._process_events` — call recovery tick before firing new events

### Architect decisions

| Event | v2 behavior |
|-------|-------------|
| `dust_storm` | Snapshot original CF; apply reduction; schedule restore at `time + duration_hours` (default: permanent if omitted) |
| `crew_rotation` | Duration defaults 24h; after expiry, `crew_rotation_active` → false (recovery rate not reverted — supplies consumed) |
| `isru_ramp_up` | Unchanged (permanent throughput boost) |

### Acceptance criteria

1. [ ] `dust_storm` with `duration_hours: 12` restores `solar_capacity_factor` after 12 sim-hours
2. [ ] Permanent dust storm (no duration) behavior unchanged from Phase 5
3. [ ] `contracts/events.yaml` documents duration semantics
4. [ ] `tests/test_contracts_events.py` covers timed recovery + integration power comparison
5. [ ] Mars scenario optionally updated with `duration_hours` on dust_storm (backward compat if omitted)

### Edge cases

1. Overlapping dust storms — second storm re-snapshots from current CF
2. Zero duration — treat as instantaneous flag-only (no CF change)
3. Event at final timestep — recovery may never fire; acceptable

---

## Sub-epic 6.4 — Optimization (T2)

**Problem:** SRD §2.3 promises optimization; only OAT sensitivity exists.

### Interfaces

- `src/astrosim/analysis/optimize.py` — `minimize_metric(config, build_simulator, *, parameter, metric_key, bounds, method)`
- `pyproject.toml` — `[project.optional-dependencies] optimize = ["scipy>=1.11"]`
- `contracts/optimization_result.schema.json` (planned)
- `examples/run_optimize.py` (new)

### Acceptance criteria

1. [ ] `minimize_metric` finds better `solar_array_kw` for positive `energy.net_kwh` on lunar scenario
2. [ ] Returns structured result: optimal value, metric achieved, iterations, success flag
3. [ ] `pip install -e ".[optimize]"` installs scipy; core install remains scipy-free
4. [ ] `tests/test_optimize.py` passes without scipy (skip or mock) OR scipy in dev extras for CI
5. [ ] `contracts/optimization_result.schema.json` validates example output
6. [ ] `examples/run_optimize.py` runnable demo

### Edge cases

1. Flat objective — optimizer returns boundary with success=false
2. Non-numeric parameter — raise `TypeError` before scipy call
3. scipy not installed — clear `ImportError` message pointing to `[optimize]` extra

### Out of scope

- Multi-objective Pareto (Phase 7 candidate)
- Global optimization across all parameters simultaneously

---

## Sub-epic 6.5 — AI Integration Hardening (T2)

**Problem:** `adapters.py` 33% coverage; no contract for LLM responses; live path untested.

### Interfaces

- `tests/test_ai_adapters.py` — mock `urllib.request` / env key
- `scripts/smoke_llm.sh` — skipped when `XAI_API_KEY` unset
- `contracts/llm_insight.schema.json` (planned) — optional structure for parsed insights

### Acceptance criteria

1. [ ] Mocked tests cover Grok adapter success, HTTP error fallback, missing key offline path
2. [ ] `scripts/smoke_llm.sh` exits 0 with key, exits 0 with skip message without key
3. [ ] `ai/AGENT.md` documents opt-in live test policy
4. [ ] No live network calls in `pytest tests/`
5. [ ] `adapters.py` coverage ≥ 70%

### Out of scope

- Natural-language scenario editing (Phase 7)
- Fine-tuned domain models

---

## Sub-epic 6.6 — Scenarios & Examples (T2)

**Problem:** PRD vision includes orbital habitats; only lunar/Mars exist; mars MC example not CI-smoked.

### Interfaces

- `scenarios/orbital_station.yaml` + `.json` — 4 crew, 4380h, reduced gravity params
- `scripts/smoke_examples.sh` — add fast mars subset OR separate `smoke_mars_quick.sh`

### Acceptance criteria

1. [ ] `orbital_station.yaml` loads, validates against `scenario.schema.json`, runs 10-step sim
2. [ ] JSON/YAML parity for orbital scenario
3. [ ] `examples/run_orbital_station.py` writes export artifacts
4. [ ] Mars smoke: MC with `num_runs=5` completes in < 15s in CI (new script or flag)
5. [ ] `scenarios/AGENT.md` lists orbital scenario

### Out of scope

- New subsystem types for microgravity
- Deep-space transit scenario (Phase 7)

---

## Sub-epic 6.7 — Community & Packaging (T2/T3)

**Problem:** PRD success metric requires community; package not pip-installable from PyPI.

### Interfaces

- `pyproject.toml` — verify `[project.urls]`, readme, classifiers
- `.github/workflows/publish.yml` (planned) — manual workflow_dispatch for PyPI
- `docs/TUTORIAL.md` or `examples/tutorial.ipynb` — 15-min walkthrough
- `docs/PLUGIN_COOKBOOK.md` — register_subsystem patterns

### Acceptance criteria

1. [ ] `pip install .` from sdist/wheel succeeds in clean venv
2. [ ] PyPI publish workflow documented; test publish to TestPyPI OR documented manual steps
3. [ ] Tutorial covers: load scenario → run → export → plot
4. [ ] Plugin cookbook covers greenhouse-style custom subsystem with cleanup
5. [ ] Version bumped to `0.2.0`; tag `v0.2.0`; CHANGELOG updated
6. [ ] README links tutorial + cookbook

### Out of scope

- ReadTheDocs hosting (optional follow-up)
- Conference paper / study publication (human-driven)

---

## Phase 6 exit criteria (AYSU gate)

All must pass before declaring Phase 6 complete:

| # | Criterion |
|---|-----------|
| E1 | `v0.1.0` and `v0.2.0` tags exist on GitHub |
| E2 | ≥ 95 tests; coverage ≥ 82% |
| E3 | All sub-epic acceptance criteria checked |
| E4 | `TASKS.md` Phase 6 all ✅ |
| E5 | No open critical/high CDD findings on Phase 6 epics |
| E6 | `contracts/README.md` lists any new schemas as active |

---

## Implementation notes

- **6.1 is human-gated** — agent prepares docs/commits; Adrian runs `git push` and confirms Actions green.
- **CI scipy** — add `optimize` extra to CI install when 6.4 lands: `pip install -e ".[dev,optimize]"`.
- **Benchmark** — store baseline in `docs/PERFORMANCE.md` as text, not committed timing artifact.
- **Breaking changes** — none expected; duration fields are optional additions.

## CDD focus areas

| Area | Risk |
|------|------|
| Event recovery | Double-restore, overlapping storms, state leaks in config.parameters |
| Optimization | scipy optional import paths; CI without scipy |
| LLM adapters | Accidental live network in pytest; credential leakage in logs |
| PyPI | Token handling in workflow; name squatting on `astrosim` |
| Perf benchmark | Flaky CI timing assertions |

## Sub-epic → implementer plan files

When starting each sub-epic, copy sections above into dedicated plans (optional):

| Sub-epic | Plan file (create on start) |
|----------|----------------------------|
| 6.1 | `docs/plans/epic-phase6-release.md` |
| 6.2 | `docs/plans/epic-phase6-quality.md` |
| 6.3 | `docs/plans/epic-phase6-events.md` |
| 6.4 | `docs/plans/epic-phase6-optimize.md` |
| 6.5 | `docs/plans/epic-phase6-ai.md` |
| 6.6 | `docs/plans/epic-phase6-scenarios.md` |
| 6.7 | `docs/plans/epic-phase6-community.md` |

## Out of scope (entire Phase 6)

- Real-time 3D rendering
- CFD/FEA integration
- Hardware-in-the-loop
- Classified data
- Multi-objective Pareto frontier
- NL scenario editor
- New physics subsystems beyond parameter tuning