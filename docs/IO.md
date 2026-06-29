# Inputs & Outputs

One-page reference for what goes into AstroSim and what comes out.  
Canonical schemas live in [`contracts/`](../contracts/README.md).

---

## Quick map

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────────┐
│ INPUT               │     │ ENGINE           │     │ OUTPUT                  │
├─────────────────────┤     ├──────────────────┤     ├─────────────────────────┤
│ scenario.yaml/json  │ ──► │ Simulator loop   │ ──► │ SimulationResult (API)  │
│ CLI flags           │     │ Subsystems       │     │ JSON / CSV export       │
│ Python Config       │     │ Budgets          │     │ PNG / HTML dashboards   │
│ Custom plugins      │     │ Events / MC      │     │ Study / insight / suite │
└─────────────────────┘     └──────────────────┘     └─────────────────────────┘
```

---

## Inputs

### 1. Scenario file (primary input)

YAML or JSON. See [SCENARIOS.md](SCENARIOS.md) for full schema.

| Section | Required | Purpose |
|---------|----------|---------|
| `simulation` | yes | `duration_hours`, `timestep_hours`, `crew_count` |
| `parameters` | no | Flat dict passed to every subsystem each step |
| `events` | no | Timed payloads → `state.flags` |
| `subsystems` | no | Subset to run; default = all built-ins |

**Built-in subsystems:** `power`, `eclss`, `thermal`, `structure`, `isru`, `compute`, `greenhouse`

**Minimal example:**

```yaml
name: Greenhouse Lunar Base
location: lunar
simulation:
  duration_hours: 168
  timestep_hours: 6
  crew_count: 4
subsystems:
  - power
  - greenhouse
  - eclss
  - thermal
parameters:
  solar_array_kw: 80
  battery_kwh: 400
  growth_rate_kg_per_hour: 0.15
```

### 2. CLI

```bash
astrosim <scenario> [options]
```

| Flag | Input effect | Output effect |
|------|--------------|---------------|
| `--output-dir DIR` | — | Write artifacts under `DIR/` |
| `--web` | — | Adds `*_dashboard.html` |
| `--no-plot` | — | Skips PNG dashboard |
| `--report` | — | Adds `study_report.md` + `.json` |
| `--insights-json` | — | Adds `*_insight.json` |
| `--monte-carlo N` | Runs N perturbed configs | Adds `*_monte_carlo_summary.json` |
| `--compare A B ...` | Multiple scenario paths | Prints table + `scenario_compare.csv` |
| `--compare-mc N` | MC runs per compare row | Adds `*_mean` / `*_std` columns |
| `--suite` | Runs 8 canonical scenarios | Writes `suite_report.json` |
| `--trade-study` | Solar/battery grid on scenario | Writes `trade_study.csv` |
| `--ask "..."` | NL edit prompt | Dry-run JSON or patched YAML (`--write`) |

### 3. Python API

```python
from astrosim.scenario import load_and_build

result = load_and_build("scenarios/greenhouse_lunar.yaml").run()
```

| Input object | Fields |
|--------------|--------|
| `SimulationConfig` | `name`, `duration_hours`, `timestep_hours`, `crew_count`, `parameters`, `events`, `subsystems` |
| Custom `Subsystem` | `update(state, dt_hours, params) -> dict[str, float]` |

---

## Outputs

### 1. Python `SimulationResult`

Returned by `Simulator.run()` / `load_and_build(...).run()`.

| Field | Type | Contents |
|-------|------|----------|
| `config` | `SimulationConfig` | Copy of run configuration |
| `history` | `list[SimulationState]` | One snapshot per timestep |
| `energy_budget` | `EnergyBudget` | `generated_kwh`, `consumed_kwh`, `net_kwh` |
| `mass_budget` | `MassBudget` | `imported_kg`, `consumed_kg`, `net_import_kg` |
| `reliability_budget` | `ReliabilityBudget` | `mission_success_probability` |
| `final_state` | `SimulationState` | Last step; `metrics` dict keyed `subsystem.field` |

Access metrics:

```python
result.final_state.metrics["eclss.food_net_import_kg"]
result.energy_budget.net_kwh
```

### 2. Standard CLI file outputs

Default directory: `output/` (or `--output-dir`).

| File | Format | Description |
|------|--------|-------------|
| `{name}.json` | JSON | Config + budgets + full history ([schema](../contracts/export_result.schema.json)) |
| `{name}.csv` | CSV | One row per timestep; columns = metrics |
| `{name}_dashboard.png` | PNG | Matplotlib 2×3 grid (unless `--no-plot`) |
| `{name}_dashboard.html` | HTML | Interactive charts (`--web`) |
| `study_report.md` | Markdown | Human-readable study (`--report`) |
| `study_report.json` | JSON | Machine-readable study metadata |
| `{name}_insight.json` | JSON | Offline/LLM insight (`--insights-json`) |
| `{name}_monte_carlo_summary.json` | JSON | Per-metric mean/std/p5/p95 (`--monte-carlo`) |
| `scenario_compare.csv` | CSV | Multi-scenario metric table (`--compare`) |
| `suite_report.json` | JSON | Canonical suite run (`--suite`) |
| `trade_study.csv` | CSV | Pareto grid (`--trade-study`) |

`{name}` = scenario name lowercased with spaces → underscores (e.g. `greenhouse_lunar_base`).

---

## Sample outputs

Generated from `scenarios/greenhouse_lunar.yaml` (168 h, 4 crew, greenhouse + ECLSS).

### Budget summary (JSON export excerpt)

```json
{
  "energy": {
    "generated_kwh": 3763.2,
    "consumed_kwh": 3836.0,
    "net_kwh": -72.8
  },
  "mass": {
    "imported_kg": 0.0,
    "produced_kg": 0.0,
    "consumed_kg": 51.55,
    "net_import_kg": 51.55
  },
  "reliability": {
    "mission_success_probability": 0.99998,
    "risk_structure": 1.53e-05
  }
}
```

### First timestep (history record)

```json
{
  "time_hours": 0,
  "step": 0,
  "mass_kg": 0.501,
  "power.generated_kwh": 134.4,
  "power.stored_kwh": 2.4,
  "greenhouse.food_supplied_kg": 1.104,
  "eclss.food_net_import_kg": 0.696,
  "eclss.water_net_kg": 0.18,
  "eclss.co2_ppm": 450.0,
  "reliability.success_probability": 0.9999995
}
```

### CSV columns (header excerpt)

```
time_hours,step,mass_kg,power.generated_kwh,power.stored_kwh,
greenhouse.food_supplied_kg,eclss.food_net_import_kg,eclss.water_net_kg,...
```

### Study report metadata (`study_report.json`)

```json
{
  "title": "Greenhouse Lunar Base",
  "scenario_path": "scenarios/greenhouse_lunar.yaml",
  "method": "deterministic",
  "duration_hours": 168,
  "crew_count": 4,
  "location": "lunar",
  "metrics": {
    "energy_net_kwh": -72.8,
    "mass_net_import_kg": 51.55,
    "mission_success_probability": 0.99998
  },
  "reproducibility_command": "astrosim scenarios/greenhouse_lunar.yaml --output-dir output/study_run"
}
```

### Offline insight (`*_insight.json`)

```json
{
  "content": "Completed 28 timesteps for 'Greenhouse Lunar Base'. Energy balance: -72.8 kWh net (3763.2 generated, 3836.0 consumed). Estimated mission success probability: 1.0000.",
  "offline": true,
  "provider": "offline"
}
```

### Scenario compare (stdout / CSV)

```
scenario_name          energy.net_kwh    mass.net_import_kg    eclss.food_net_import_kg
Greenhouse Lunar Base  -72.8             51.55                 0.696
Lunar Base Alpha       -1746.0           -2081.15              1.368
```

### Suite report row (`suite_report.json` excerpt)

```json
{
  "scenarios": [
    {
      "scenario_name": "Greenhouse Lunar Base",
      "energy_net_kwh": -72.8,
      "mass_net_import_kg": 51.55,
      "mission_success_probability": 0.99998,
      "error": null
    }
  ]
}
```

---

## Interpreting outputs (implications & verdict)

Raw numbers are not conclusions. AstroSim now adds rule-based **Implications** and **Verdict** when you use `--report` or offline CLI insights.

| Signal | Meaning | Typical implication |
|--------|---------|---------------------|
| `energy.net_kwh < 0` | Power deficit over mission | Increase `solar_array_kw` or reduce load |
| `mass.net_import_kg > 0` | Net logistics burden | Consumables exceed local production |
| `mass.net_import_kg < 0` | Net local production | ISRU/recycling offsets imports |
| `eclss.food_net_import_kg` high | Food resupply needed | Add greenhouse or accept food logistics |
| `greenhouse.food_supplied_kg` > 0 | Local food credit | Lowers food net import per step |
| `mission_success_probability` < 0.99 | Elevated structure risk | Review shielding / duration |

### Example verdict — `greenhouse_lunar.yaml` (168 h, 4 crew)

**Key results:** energy net **−72.8 kWh** · mass net import **+51.5 kg** · food net import **0.70 kg/step** (vs 1.80 without greenhouse) · reliability **0.99998**

**Implications:**
- Small energy deficit — close to balance; greenhouse + ECLSS load nearly covered by 80 kW solar.
- Positive mass import — still need consumables, but greenhouse cuts food import ~39% per step.
- Greenhouse costs ~2 kW — trades power for reduced food logistics.
- Reliability high — micrometeoroid risk negligible at 168 h.

**Verdict:** *Power system needs modest upgrade before scaling crew or duration. Greenhouse helps but logistics remain net-positive.*

Generate this automatically:

```bash
astrosim scenarios/greenhouse_lunar.yaml --report --output-dir output/analysis
grep -A5 "## Verdict" output/analysis/study_report.md
```

---

## Reproduce these samples

```bash
cd astrosim
pip install -e ".[dev]"

# Standard run
astrosim scenarios/greenhouse_lunar.yaml --web --report --insights-json \
  --output-dir output/io_sample

# Compare two scenarios
astrosim --compare scenarios/greenhouse_lunar.yaml scenarios/lunar_base.yaml \
  --output-dir output/io_sample

# Full canonical suite
astrosim --suite --output-dir output/io_sample
```

---

## Related docs

| Doc | Topic |
|-----|-------|
| [SCENARIOS.md](SCENARIOS.md) | Input schema & parameters |
| [API.md](API.md) | Python interfaces |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Engine data flow diagram |
| [contracts/README.md](../contracts/README.md) | JSON schemas for exports |
| [STUDY_TEMPLATE.md](STUDY_TEMPLATE.md) | Writing formal studies |