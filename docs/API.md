# AstroSim Public API

Reference for the primary interfaces exposed by AstroSim v0.1.0.

## Quick Reference

```python
from astrosim.scenario import load_scenario, build_simulator, load_and_build
from astrosim.engine.simulator import Simulator, SimulationResult
from astrosim.engine.state import SimulationConfig, SimulationState
from astrosim.subsystems import Subsystem, register_subsystem, build_subsystems
from astrosim.ai.hooks import AIHooks, InsightRequest, LLMClient
```

---

## Scenario Loading

### `load_scenario(path) → SimulationConfig`

Load a YAML or JSON scenario file.

```python
from astrosim.scenario import load_scenario

config = load_scenario("scenarios/lunar_base.yaml")
print(config.name, config.num_steps)
```

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `path` | `str \| Path` | Path to `.yaml`, `.yml`, or `.json` file |

**Returns:** `SimulationConfig`

**Raises:** `FileNotFoundError`, `KeyError` (missing `simulation`), YAML/JSON parse errors

---

### `build_simulator(config, subsystems=None) → Simulator`

Construct a `Simulator` from a config. Uses `config.subsystems` or all defaults.

```python
from astrosim.scenario import load_scenario, build_simulator

config = load_scenario("scenarios/mars_habitat.yaml")
simulator = build_simulator(config)
```

**Parameters**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `config` | `SimulationConfig` | — | Parsed scenario config |
| `subsystems` | `list[Subsystem] \| None` | `None` | Explicit subsystem instances |

---

### `load_and_build(path) → Simulator`

Convenience: `build_simulator(load_scenario(path))`.

```python
from astrosim.scenario import load_and_build

result = load_and_build("scenarios/lunar_base.yaml").run()
```

---

## Simulator

### `Simulator`

Orchestrates subsystem updates over discrete timesteps.

```python
from astrosim.engine.simulator import Simulator
from astrosim.engine.state import SimulationConfig
from astrosim.subsystems import DEFAULT_SUBSYSTEMS

config = SimulationConfig(
    name="test",
    duration_hours=24,
    timestep_hours=6,
    crew_count=2,
    parameters={"solar_array_kw": 40},
)

simulator = Simulator(config, DEFAULT_SUBSYSTEMS)
result = simulator.run()
```

#### Constructor

```python
Simulator(config: SimulationConfig, subsystems: list[Subsystem])
```

**Attributes**

| Attribute | Type | Description |
|-----------|------|-------------|
| `config` | `SimulationConfig` | Run configuration |
| `subsystems` | `list[Subsystem]` | Active subsystem instances |
| `energy_budget` | `EnergyBudget` | Cumulative energy accounting |
| `mass_budget` | `MassBudget` | Cumulative mass accounting |
| `reliability_budget` | `ReliabilityBudget` | Risk accumulation |
| `event_queue` | `EventQueue` | Scheduled events |

#### `run() → SimulationResult`

Execute all timesteps and return history plus budgets.

---

### `SimulationResult`

| Attribute / Property | Type | Description |
|---------------------|------|-------------|
| `config` | `SimulationConfig` | Original config |
| `history` | `list[SimulationState]` | Per-step snapshots |
| `energy_budget` | `EnergyBudget \| None` | Final energy totals |
| `mass_budget` | `MassBudget \| None` | Final mass totals |
| `reliability_budget` | `ReliabilityBudget \| None` | Final reliability |
| `final_state` | `SimulationState \| None` | Last history entry |

---

### `SimulationConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Scenario name |
| `duration_hours` | `float` | — | Total duration |
| `timestep_hours` | `float` | — | Step size |
| `crew_count` | `int` | `0` | Crew size |
| `location` | `str` | `"lunar"` | Environment |
| `parameters` | `dict[str, Any]` | `{}` | Subsystem params |
| `events` | `list[SimulationEvent]` | `[]` | Scheduled events |
| `subsystems` | `list[str] \| None` | `None` | Subsystem name filter |

**Property:** `num_steps → int`

---

### `SimulationState`

Mutable state passed between subsystems each timestep.

| Field | Type | Description |
|-------|------|-------------|
| `time_hours` | `float` | Current simulation time |
| `step` | `int` | Step index (0-based) |
| `energy_kwh` | `float` | Global energy storage |
| `mass_kg` | `float` | Global mass tracker |
| `crew_count` | `int` | Active crew |
| `subsystem_outputs` | `dict[str, dict[str, float]]` | Raw per-subsystem outputs |
| `metrics` | `dict[str, float]` | Flattened `subsystem.field` keys |
| `flags` | `dict[str, bool]` | Event and runtime flags |
| `events_fired` | `list[str]` | Names of fired events |

**Method:** `record_subsystem(name, outputs)` — internal use by `Simulator`

---

## Subsystem

### `Subsystem` (abstract base class)

All habitat models implement this interface.

```python
from astrosim.subsystems import Subsystem
from astrosim.engine.state import SimulationState
from typing import Any

class MySubsystem(Subsystem):
    name = "my_subsystem"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        return {"my_metric": 1.0}
```

#### Required

| Member | Description |
|--------|-------------|
| `name: str` | Unique registry identifier |
| `update(state, dt_hours, params) → dict[str, float]` | Advance one timestep |

#### Provided

| Member | Description |
|--------|-------------|
| `get_state() → dict[str, float]` | Copy of internal `_local_state` |
| `step(state, dt_hours, params)` | Calls `update()` and stores outputs |

Incomplete subclasses raise `TypeError` at instantiation.

---

## Plugin Registry

### `register_subsystem(cls) → Type[Subsystem]`

Decorator that registers a subsystem class by `cls.name`.

```python
from astrosim.subsystems import register_subsystem, Subsystem

@register_subsystem
class GreenhouseSubsystem(Subsystem):
    name = "greenhouse"

    def update(self, state, dt_hours, params):
        growth = params.get("growth_rate", 0.1) * dt_hours
        return {"biomass_kg": growth}
```

### `get_subsystem(name) → Subsystem`

Return a new instance of the named subsystem.

**Raises:** `KeyError` if not registered

### `list_subsystems() → list[str]`

Sorted list of registered subsystem names.

### `build_subsystems(names=None) → list[Subsystem]`

Instantiate subsystems. `None` returns all registered.

```python
from astrosim.subsystems import build_subsystems

subset = build_subsystems(["power", "eclss"])
```

---

## AIHooks

LLM integration bridge for simulation insights and optimization.

```python
from astrosim.ai.hooks import AIHooks, InsightRequest

ai = AIHooks()  # offline mode
insights = ai.generate_insights(InsightRequest(result=result))
suggestions = ai.suggest_optimizations(result)
```

### Constructor

```python
AIHooks(client: LLMClient | None = None)
```

Pass a client implementing `LLMClient` for live LLM calls; otherwise offline heuristics are used.

### `LLMClient` (Protocol)

```python
class LLMClient(Protocol):
    def complete(self, prompt: str) -> str: ...
```

### Methods

#### `build_context(result) → str`

Format simulation summary (scenario, budgets, final metrics) as prompt context.

#### `generate_insights(request) → str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `InsightRequest` | `result` + optional `question` |

Returns insight text. Uses `client.complete()` when a client is provided.

#### `suggest_optimizations(result) → list[OptimizationSuggestion]`

Rule-based suggestions for energy deficit or mass import. Each suggestion includes `parameter`, `current_value`, `suggested_value`, and `rationale`.

### `InsightRequest`

| Field | Type | Default |
|-------|------|---------|
| `result` | `SimulationResult` | — |
| `question` | `str` | `"Summarize key risks and optimization opportunities."` |

### `OptimizationSuggestion`

| Field | Type |
|-------|------|
| `parameter` | `str` |
| `current_value` | `float` |
| `suggested_value` | `float` |
| `rationale` | `str` |

---

## CLI

```bash
astrosim <scenario.yaml> [--output-dir DIR] [--no-plot] [--web]
```

Installed via `[project.scripts]` as `astrosim.cli:main`.

---

## Export & Visualization

```python
from astrosim.export.formats import export_json, export_csv
from astrosim.visualization.dashboard import plot_dashboard
from astrosim.visualization.web import render_web_dashboard

export_json(result, "output/results.json")
export_csv(result, "output/results.csv")
plot_dashboard(result, "output/dashboard.png")
render_web_dashboard(result, "output/dashboard.html")
```

---

## Analysis

```python
from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.analysis.sensitivity import one_at_a_time_sensitivity
from astrosim.scenario import build_simulator

mc = MonteCarloRunner(config, build_simulator, seed=42)
mc_result = mc.run(num_runs=50, perturbation=0.1)

sens = one_at_a_time_sensitivity(
    config, build_simulator,
    parameter="solar_array_kw",
    metric_key="power.generated_kwh",
)
```

---

## Version

```python
import astrosim
print(astrosim.__version__)  # "0.1.0"
```

---

## Related Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) — system design
- [SCENARIOS.md](SCENARIOS.md) — scenario schema
- [CONTRIBUTING.md](CONTRIBUTING.md) — development guide