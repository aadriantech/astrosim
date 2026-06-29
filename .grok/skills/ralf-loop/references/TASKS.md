# AstroSim RALF Task Tracker

**Legend:** ✅ done · ⬜ pending  
**Work order:** `1.4.3.x` → `1.5.3.x` → `1.3.2.x` → Phase 2 → Phase 3 → Phase 4

---

## Phase 1 — MVP Core

### 1.1 Project Foundation

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.1.1.1 | Package scaffold | `pyproject.toml` with hatchling, Python ≥3.10, MIT license | ✅ |
| 1.1.1.2 | Source layout | `src/astrosim/` package with `__init__.py` | ✅ |
| 1.1.2.1 | LICENSE | MIT license file present | ✅ |
| 1.1.2.2 | README | Quick start with install, examples, CLI usage | ✅ |
| 1.1.3.1 | PRD | `docs/PRD.md` defines MVP scope and goals | ✅ |
| 1.1.3.2 | SRD | `docs/SRD.md` defines functional requirements | ✅ |

### 1.2 Simulation Engine (SRD §2.1)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.2.1.1 | SimulationState | Mutable state with time, energy, mass, metrics, flags | ✅ |
| 1.2.1.2 | SimulationConfig | Configurable duration, Δt, crew, location, parameters | ✅ |
| 1.2.1.3 | Metric prefixing | `record_subsystem()` prefixes keys as `{name}.{field}` | ✅ |
| 1.2.2.1 | Simulator loop | Discrete time-step over `num_steps` | ✅ |
| 1.2.2.2 | History snapshots | Each step appended to `SimulationResult.history` | ✅ |
| 1.2.2.3 | final_state property | Returns last history entry | ✅ |
| 1.2.3.1 | SimulationEvent | Scheduled event with time, name, payload | ✅ |
| 1.2.3.2 | EventQueue | `due_at()` fires events at matching timestep | ✅ |
| 1.2.3.3 | Event flags | Payload merged into `state.flags` | ✅ |
| 1.2.4.1 | MonteCarloRunner | Repeated runs with parameter perturbation | ✅ |
| 1.2.4.2 | Config perturbation | Numeric params scaled by uniform noise | ✅ |
| 1.2.4.3 | MC summary stats | mean, std, p5, p95 per metric | ✅ |

### 1.3 Subsystem Modules (SRD §2.2)

#### 1.3.1 Power

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.1.1 | Solar generation | `generated_kwh = solar_kw × CF × dt` | ✅ |
| 1.3.1.2 | Battery clamping | `stored_kwh` clamped to ±`battery_kwh` | ✅ |
| 1.3.1.3 | Crew load | `load_kw = base + crew × 0.5` | ✅ |

#### 1.3.2 ECLSS *(deferred in work order — after 1.5.3)*

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.2.1 | O₂ consumption | `o2_consumed_kg = crew × rate × days` | ✅ |
| 1.3.2.2 | Water net | `water_net_kg` reflects consumption minus recovery | ✅ |
| 1.3.2.3 | Food & waste | Food consumed and waste generated/recycled tracked | ✅ |
| 1.3.2.4 | CO₂ accumulation | `co2_ppm` rises across timesteps | ✅ |
| 1.3.2.5 | Mass state update | `state.mass_kg` updated from net flows | ✅ |

#### 1.3.3 Thermal

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.3.1 | Delta-T model | `delta_t_c = internal_target − ambient` | ✅ |
| 1.3.3.2 | Crew heat load | Heat load scales with crew count | ✅ |

#### 1.3.4 ISRU

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.4.1 | Regolith throughput | `processed = throughput × dt` | ✅ |
| 1.3.4.2 | Extraction yields | O₂ and water produced from processed mass | ✅ |

#### 1.3.5 Structure

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.5.1 | Volume metrics | Pressurized volume and hull mass reported | ✅ |
| 1.3.5.2 | Step risk | `micrometeoroid_step_risk` per timestep | ✅ |
| 1.3.5.3 | Cumulative risk | `micrometeoroid_cumulative_risk` accumulates across steps | ✅ |

#### 1.3.6 Compute

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.6.1 | AI power draw | Power scales with `ai_utilization` | ✅ |
| 1.3.6.2 | Radiation dose | `dose_sv_step` reduced by shielding factor | ✅ |
| 1.3.6.3 | BER tracking | `bit_error_rate` derived from dose | ✅ |

#### 1.3.7 Plugin System

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.3.7.1 | Subsystem ABC | Abstract `update()` + `get_state()` interface | ✅ |
| 1.3.7.2 | Registry decorator | `@register_subsystem` registers by `name` | ✅ |
| 1.3.7.3 | build_subsystems | Factory instantiates by name list or all | ✅ |

### 1.4 Budgeting & Analysis (SRD §2.3)

#### 1.4.1 Energy Budget

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.4.1.1 | Accumulate gen/consumed | Tracks `generated_kwh` and `consumed_kwh` | ✅ |
| 1.4.1.2 | Subsystem power draw | `power_kw` outputs added to `by_subsystem` | ✅ |
| 1.4.1.3 | net_kwh + summary | `net_kwh` property and `summary()` dict | ✅ |

#### 1.4.2 Mass Budget

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.4.2.1 | Flow accumulation | ECLSS/ISRU produced and consumed tracked | ✅ |
| 1.4.2.2 | net_import_kg | `consumed − produced + imported` | ✅ |
| 1.4.2.3 | summary() | Returns imported, produced, consumed, net | ✅ |

#### 1.4.3 Reliability Budget *(first priority)*

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.4.3.1 | Record step risk | `record_step()` accumulates `micrometeoroid_step_risk` | ✅ |
| 1.4.3.2 | Cumulative risk source | Structure outputs `micrometeoroid_cumulative_risk` | ✅ |
| 1.4.3.3 | Mission success | `mission_success_probability = exp(−Σrisk)` | ✅ |
| 1.4.3.4 | Reliability summary | `summary()` returns probability + per-subsystem risks | ✅ |

#### 1.4.4 Sensitivity Analysis

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.4.4.1 | OAT sweep | `one_at_a_time_sensitivity()` varies one param | ✅ |
| 1.4.4.2 | Elasticity | Elasticity computed from metric response | ✅ |

### 1.5 UI, Export & Scenarios (SRD §2.4)

#### 1.5.1 Scenario Loading

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.5.1.1 | YAML loader | `load_scenario()` parses `.yaml` files | ✅ |
| 1.5.1.2 | JSON loader | `load_scenario()` parses `.json` files | ✅ |
| 1.5.1.3 | Events in config | `config_from_dict()` builds `SimulationEvent` list | ✅ |
| 1.5.1.4 | load_and_build | One-call scenario → `Simulator` factory | ✅ |

#### 1.5.2 Export

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.5.2.1 | export_json | JSON with config, budgets, history | ✅ |
| 1.5.2.2 | export_csv | CSV time-series from history | ✅ |
| 1.5.2.3 | result_to_dataframe | History → pandas DataFrame | ✅ |

#### 1.5.3 Visualization *(second priority)*

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 1.5.3.1 | Matplotlib dashboard | 4-panel `plot_dashboard()` PNG output | ✅ |
| 1.5.3.2 | HTML web dashboard | Self-contained `render_web_dashboard()` | ✅ |
| 1.5.3.3 | CLI --web flag | `astrosim scenario.yaml --web` generates HTML | ✅ |
| 1.5.3.4 | Example script outputs | `run_lunar_base.py` writes json/csv/png/html | ✅ |
| 1.5.3.5 | Web ECLSS chart | HTML dashboard includes ECLSS water-net series | ✅ |
| 1.5.3.6 | Web thermal chart | HTML dashboard includes thermal heat-load series | ✅ |

---

## Phase 2 — Test Coverage (TDD)

### 2.1 Unit Tests — Budgeting

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 2.1.1.1 | Mass budget tests | `tests/test_mass_budget.py` covers accumulate + net | ✅ |
| 2.1.1.2 | Reliability budget tests | `tests/test_reliability_budget.py` covers record + probability | ✅ |
| 2.1.1.3 | Mass import suggestion | AI hook suggests water_recovery when net_import > 0 | ✅ |

### 2.2 Unit Tests — Export & CLI

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 2.2.1.1 | Export JSON round-trip | `tests/test_export.py` validates JSON structure | ✅ |
| 2.2.1.2 | Export CSV columns | CSV contains `time_hours` and metric columns | ✅ |
| 2.2.1.3 | CLI smoke test | `tests/test_cli.py` runs astrosim on lunar scenario | ✅ |

### 2.3 Integration Tests — Engine

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 2.3.1.1 | Simulator step count | History length equals `num_steps` | ✅ |
| 2.3.1.2 | Budget attachment | Result includes energy, mass, reliability budgets | ✅ |
| 2.3.1.3 | Metric key prefixing | Final metrics use `{subsystem}.{field}` keys | ✅ |
| 2.3.1.4 | Event integration | Scheduled events appear in `events_fired` | ✅ |

### 2.4 Integration Tests — Subsystems

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 2.4.1.1 | Power unit tests | `tests/test_power.py` passes | ✅ |
| 2.4.1.2 | ECLSS unit tests | `tests/test_eclss.py` passes | ✅ |
| 2.4.1.3 | Thermal unit tests | `tests/test_thermal.py` passes | ✅ |
| 2.4.1.4 | ISRU unit tests | `tests/test_isru.py` passes | ✅ |
| 2.4.1.5 | Compute unit tests | `tests/test_compute.py` passes | ✅ |
| 2.4.1.6 | Structure unit tests | `tests/test_structure.py` passes (cumulative risk) | ✅ |
| 2.4.1.7 | Subsystem base tests | `tests/test_subsystem_base.py` passes | ✅ |

### 2.5 Integration Tests — Analysis & AI

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 2.5.1.1 | Sensitivity test | `test_sensitivity_analysis` in test_srd_features | ✅ |
| 2.5.1.2 | Monte Carlo reproducibility | Same seed → identical summary | ✅ |
| 2.5.1.3 | Monte Carlo seed variance | Different seeds can produce different summaries | ✅ |
| 2.5.1.4 | AI offline insights | Non-empty insights without LLM client | ✅ |
| 2.5.1.5 | AI solar suggestion | Energy deficit triggers solar_array_kw suggestion | ✅ |
| 2.5.1.6 | Plugin registry test | Custom `@register_subsystem` works | ✅ |
| 2.5.1.7 | Web dashboard test | HTML contains "AstroSim Dashboard" | ✅ |

### 2.6 Scenario Tests

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 2.6.1.1 | Lunar YAML scenario | Loads with correct name, crew, location, steps | ✅ |
| 2.6.1.2 | Mars YAML scenario | Loads with correct name, crew, location | ✅ |
| 2.6.1.3 | Lunar JSON scenario | JSON loader reads parameters and events | ✅ |

---

## Phase 3 — Examples & Polish

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 3.1.1.1 | Lunar base example | `examples/run_lunar_base.py` runs end-to-end | ✅ |
| 3.1.1.2 | Mars habitat example | `examples/run_mars_habitat.py` with Monte Carlo | ✅ |
| 3.1.2.1 | Mars scenario events | `mars_habitat.yaml` includes scheduled events | ✅ |
| 3.1.3.1 | Lunar scenario parity | JSON and YAML lunar scenarios structurally aligned | ✅ |
| 3.1.3.2 | Mars scenario parity | JSON and YAML mars scenarios structurally aligned | ✅ |
| 3.2.1.1 | CLI --monte-carlo flag | CLI option runs MC and writes summary JSON | ✅ |
| 3.2.1.2 | AI optimization in CLI | CLI prints optimization suggestions | ✅ |
| 3.3.1.1 | pyproject dev extras | `pip install -e ".[dev]"` installs pytest | ✅ |
| 3.3.1.2 | Test coverage gate | pytest-cov reports ≥80% line coverage | ✅ |

---

## Phase 4 — Release Readiness

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 4.1.1.1 | CHANGELOG | `CHANGELOG.md` documents v0.1.0 features | ✅ |
| 4.1.1.2 | CI workflow | GitHub Actions runs pytest on push/PR | ✅ |
| 4.1.1.3 | Coverage in CI | CI fails if coverage drops below threshold | ✅ |
| 4.2.1.1 | SRD test matrix | README or docs map SRD reqs → tests | ✅ |
| 4.2.1.2 | Contributing guide | `CONTRIBUTING.md` with dev setup and RALF loop | ✅ |
| 4.3.1.1 | Version tag prep | `pyproject.toml` version matches release | ✅ |
| 4.3.1.2 | PyPI metadata | classifiers, keywords, authors complete | ✅ |
| 4.4.1.1 | Full test suite green | `pytest tests/ -q` exits 0 | ✅ |

---

## Phase 5 — Contracts, Events & Hardening

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 5.1.1.1 | Export result schema | `contracts/export_result.schema.json` + tests | ✅ |
| 5.1.1.2 | CI example smoke | `scripts/smoke_examples.sh` in workflow | ✅ |
| 5.1.1.3 | Registry test cleanup | `unregister_subsystem()` + tests | ✅ |
| 5.2.1.1 | Active dust_storm handler | Reduces `solar_capacity_factor` | ✅ |
| 5.2.1.2 | Active crew_rotation handler | Sets flag + bumps water recovery | ✅ |
| 5.2.1.3 | Event catalog sync | `contracts/events.yaml` matches handlers | ✅ |
| 5.3.1.1 | Matplotlib dashboard test | `tests/test_visualization.py` PNG assert | ✅ |
| 5.3.1.2 | Remove unused scipy dep | Dropped from `pyproject.toml` | ✅ |

---

## Phase 6 — Post-MVP Growth (v0.2.0)

**Master plan:** `docs/plans/epic-phase6.md`  
**Work order:** 6.1 → 6.2 → 6.3 → 6.4 → 6.5 → 6.6 → 6.7

### 6.1 Release & Distribution (T3)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.1.1.1 | Push to GitHub | `main` on `aadriantech/astrosim` | ✅ |
| 6.1.1.2 | Tag v0.1.0 | Annotated tag pushed | ✅ |
| 6.1.1.3 | CHANGELOG 0.1.0 | Unreleased items promoted | ✅ |
| 6.1.1.4 | RELEASE.md | Push/tag/verify documented | ✅ |
| 6.1.1.5 | CI green on remote | GitHub Actions pass on main | ✅ |

### 6.2 Quality & Performance (T2)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.2.1.1 | Benchmark script | `scripts/benchmark_sim.py` times 1-year sim | ✅ |
| 6.2.1.2 | CLI unit coverage | `cli.py` ≥ 60% via extracted helpers | ✅ |
| 6.2.1.3 | Plugin smoke isolation | `custom_subsystem` no registry pollution | ✅ |
| 6.2.1.4 | PERFORMANCE.md | Baseline wall-time documented | ✅ |

### 6.3 Event Semantics v2 (T2)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.3.1.1 | Timed dust_storm recovery | CF restores after `duration_hours` | ✅ |
| 6.3.1.2 | crew_rotation duration | `crew_rotation_active` expires | ✅ |
| 6.3.1.3 | events.yaml contract update | Duration semantics documented | ✅ |
| 6.3.1.4 | Event recovery tests | Unit + integration in test_contracts_events | ✅ |

### 6.4 Optimization (T2)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.4.1.1 | minimize_metric API | `analysis/optimize.py` | ✅ |
| 6.4.1.2 | scipy optional extra | `[optimize]` in pyproject.toml | ✅ |
| 6.4.1.3 | optimization_result schema | Contract + validation test | ✅ |
| 6.4.1.4 | run_optimize example | Runnable demo script | ✅ |
| 6.4.1.5 | test_optimize.py | Green in CI with optimize extra | ✅ |

### 6.5 AI Integration Hardening (T2)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.5.1.1 | Mocked adapter tests | `tests/test_ai_adapters.py` | ✅ |
| 6.5.1.2 | smoke_llm.sh | Opt-in live test, skip without key | ✅ |
| 6.5.1.3 | adapters.py coverage | ≥ 70% | ✅ |
| 6.5.1.4 | llm_insight schema | Planned contract active | ✅ |

### 6.6 Scenarios & Examples (T2)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.6.1.1 | orbital_station scenario | YAML + JSON + schema validation | ✅ |
| 6.6.1.2 | run_orbital_station.py | Example script + export | ✅ |
| 6.6.1.3 | Mars quick smoke | MC num_runs=5 in < 15s CI script | ✅ |
| 6.6.1.4 | Scenario parity tests | Orbital in test_contracts_parity | ✅ |

### 6.7 Community & Packaging (T2/T3)

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.7.1.1 | Wheel/sdist build | `pip install .` in clean venv | ✅ |
| 6.7.1.2 | PyPI workflow | publish.yml or documented manual publish | ✅ |
| 6.7.1.3 | Tutorial | TUTORIAL.md or tutorial.ipynb | ✅ |
| 6.7.1.4 | Plugin cookbook | PLUGIN_COOKBOOK.md | ✅ |
| 6.7.1.5 | Release v0.2.0 | Version bump, tag, CHANGELOG | ✅ |

### Phase 6 exit gate

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 6.0.1 | Phase 6 AYSU | All sub-epics ✅, ≥95 tests, ≥82% cov | ✅ |

---

## Phase 7 — Advanced Analysis & AI (v0.3.0)

**Master plan:** `docs/plans/epic-phase7.md`  
**Precondition:** `bash scripts/integrity_check.sh` green

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 7.1.1.1 | Pareto trade study API | `analysis/pareto.py` + CSV export | ✅ |
| 7.1.1.2 | trade_study schema | Contract + tests | ✅ |
| 7.2.1.1 | deep_space_transit scenario | YAML + JSON parity | ✅ |
| 7.3.1.1 | NL scenario editor | `ai/scenario_editor.py` mocked tests | ✅ |
| 7.4.1.1 | ISRU power coupling | Throughput tied to energy budget | ✅ |
| 7.5.1.1 | tutorial.ipynb | Colab-ready notebook | ✅ |
| 7.6.1.1 | Release v0.3.0 | Tag + STUDY_TEMPLATE.md | ✅ |

---

## Phase 8 — CI Restore & Production Hardening (v0.4.0)

**Master plan:** `docs/plans/epic-phase8.md`  
**Precondition:** SSH remote (`github.com-aadriantech`) configured

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 8.1.1.1 | SSH push remote | `git@github.com-aadriantech:aadriantech/astrosim.git` | ✅ |
| 8.1.1.2 | CI workflows restored | `.github/workflows/` on remote | ✅ |
| 8.1.1.3 | pyproject.toml fix | classifiers/deps under `[project]`; CI install green | ✅ |
| 8.2.1.1 | Trade study CLI | `astrosim --trade-study` flag | ✅ |
| 8.2.1.2 | run_trade_study example | `examples/run_trade_study.py` | ✅ |
| 8.3.1.1 | NL editor battery/duration | Parse `battery_kwh`, `duration_hours` intents | ✅ |
| 8.4.1.1 | MC trade envelope | `monte_carlo_runs` on `run_trade_study()` | ✅ |
| 8.4.1.2 | trade_study schema std fields | `metric_a_std`, `metric_b_std` in contract | ✅ |
| 8.5.1.1 | CI badge | README Actions badge | ✅ |
| 8.5.1.2 | Release v0.4.0 | Tag + CHANGELOG | ✅ |
| 8.5.1.3 | PyPI publish | `verify_pypi_ready.sh` + `publish.yml` (token for live upload) | ✅ |

### Phase 8 exit gate

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 8.0.1 | Phase 8 AYSU | ≥121 tests, integrity green, CI green on main | ✅ |

---

## Phase 9 — Research Workflows & Biosphere Closure (v0.5.0)

**Master plan:** `docs/plans/epic-phase9.md`  
**Precondition:** Phase 8 exit gate green

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 9.1.1.1 | PyPI publish | PyPI-ready verification in CI | ✅ |
| 9.2.1.1 | Greenhouse built-in | `subsystems/greenhouse.py` + contract manifest | ✅ |
| 9.3.1.1 | ECLSS food loop | `food_net_import_kg`; `greenhouse_lunar` scenario | ✅ |
| 9.4.1.1 | Study report export | `render_study_report()` + CLI `--report` | ✅ |
| 9.5.1.1 | Scenario compare | `compare_scenarios()` + CLI `--compare` | ✅ |
| 9.6.1.1 | NL editor write-back | `--ask --write` patched YAML | ✅ |
| 9.7.1.1 | Release v0.5.0 | Tag + CHANGELOG + AGENT sync | ✅ |

### Phase 9 exit gate

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 9.0.1 | Phase 9 AYSU | ≥130 tests, ≥85% cov, CDD approve 9.2–9.5 | ✅ |

---

## Phase 10 — Docs Site & Interactive Dashboard (v0.6.0)

**Master plan:** `docs/plans/epic-phase10.md`

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 10.1.1.1 | Wheel build CI smoke | `scripts/smoke_wheel.sh` in CI | ✅ |
| 10.2.1.1 | MkDocs site | `scripts/build_docs.sh` green | ✅ |
| 10.3.1.1 | Dashboard v2 | Food charts + study report embed | ✅ |
| 10.4.1.1 | Scenario suite | `run_scenario_suite()` + `--suite` | ✅ |
| 10.5.1.1 | greenhouse_mars | YAML + JSON parity | ✅ |
| 10.6.1.1 | Release v0.6.0 | CHANGELOG (bundled in v0.7.0 tag) | ✅ |

---

## Phase 11 — Closed-Loop Resources & AI Export (v0.7.0)

**Master plan:** `docs/plans/epic-phase11.md`

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 11.1.1.1 | ISRU water loop | `water_supplied_kg`; lower water_net | ✅ |
| 11.2.1.1 | Insight JSON export | `llm_insight.schema.json` + `--insights-json` | ✅ |
| 11.3.1.1 | MC compare | `--compare-mc N` mean/std columns | ✅ |
| 11.4.1.1 | NL ISRU intents | regolith + isru power parse | ✅ |
| 11.5.1.1 | mars_closed_loop | Scenario + example script | ✅ |
| 11.6.1.1 | Release v0.7.0 | Tag + AGENT sync | ✅ |

### Phase 11 exit gate

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 11.0.1 | Phase 11 AYSU | ≥170 tests target (158 shipped), ≥85% cov | ✅ |

---

## Phase 12 — Distribution & Published Study (v0.8.0)

**Master plan:** `docs/plans/epic-phase12.md`

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 12.1.1.1 | PyPI-ready verify | `scripts/verify_pypi_ready.sh` in CI | ✅ |
| 12.2.1.1 | GitHub Pages docs | `.github/workflows/docs.yml` | ✅ |
| 12.3.1.1 | Example study | `docs/studies/lunar_energy_trade.md` | ✅ |
| 12.4.1.1 | Release v0.8.0 | Bundled in v1.0.0 | ✅ |

---

## Phase 13 — O₂ Closed-Loop & Orbital Biosphere (v0.9.0)

**Master plan:** `docs/plans/epic-phase13.md`

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 13.1.1.1 | ISRU O₂ loop | `o2_net_import_kg` | ✅ |
| 13.2.1.1 | orbital_greenhouse | YAML + JSON parity | ✅ |
| 13.3.1.1 | Closed-loop audit | `test_closed_loop_audit.py` | ✅ |
| 13.4.1.1 | Release v0.9.0 | Bundled in v1.0.0 | ✅ |

---

## Phase 14 — v1.0.0 Project Completion

**Master plan:** `docs/plans/epic-phase14.md`

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| 14.1.1.1 | ROADMAP.md | Phases 1–14 listed complete | ✅ |
| 14.2.1.1 | TASKS all ✅ | No ⬜ remaining | ✅ |
| 14.3.1.1 | AYSU gate | integrity + CI green | ✅ |
| 14.4.1.1 | Release v1.0.0 | Tag on GitHub | ✅ |

### Project exit gate

| ID | Task | Acceptance | Status |
|----|------|------------|--------|
| P.0.1 | AstroSim 1.0 complete | PRD metrics met; roadmap closed | ✅ |

---

## Quick Reference

- **Next incomplete (work order):** none — **all phases complete** (v1.0.0)
- **Master plan:** `docs/ROADMAP.md`
- **Integrity gate:** `bash scripts/integrity_check.sh`
- **Push:** `bash scripts/push_github.sh` (SSH)
- **Verify command:** `cd /home/adrianlos/projects/astrosim && PYTHONPATH=src python3 -m pytest tests/ -q`
- **Fallback verify:** `python3 -m py_compile src/astrosim/subsystems/structure.py`