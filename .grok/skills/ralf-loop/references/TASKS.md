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

## Quick Reference

- **Next incomplete (work order):** none — MVP + Phase 5 complete
- **Blocked by:** GitHub push (credentials on host)
- **Verify command:** `cd /home/adrianlos/projects/astrosim && PYTHONPATH=src python3 -m pytest tests/ -q`
- **Fallback verify:** `python3 -m py_compile src/astrosim/subsystems/structure.py`