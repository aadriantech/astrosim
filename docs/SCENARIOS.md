# Scenario Format

AstroSim scenarios are YAML or JSON files that define simulation duration, crew, parameters, events, and optional subsystem selection.

## File Locations

Built-in examples live in `scenarios/`:

- `lunar_base.yaml` / `lunar_base.json` — crewed lunar outpost
- `mars_habitat.yaml` — Mars surface habitat

Load a scenario:

```bash
astrosim scenarios/lunar_base.yaml --web
```

```python
from astrosim.scenario import load_and_build

simulator = load_and_build("scenarios/lunar_base.yaml")
result = simulator.run()
```

## Schema

### Top-Level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | no | `"unnamed"` | Human-readable scenario name |
| `location` | string | no | `"unknown"` | Environment label (`lunar`, `mars`, etc.) |
| `description` | string | no | — | Free-text description (not used by engine) |
| `simulation` | object | **yes** | — | Core timing and crew settings |
| `events` | array | no | `[]` | Scheduled simulation events |
| `parameters` | object | no | `{}` | Subsystem parameter overrides |
| `subsystems` | array of strings | no | all registered | Subset of subsystem names to run |

### `simulation` Object

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `duration_hours` | number | **yes** | — | Total simulated time (hours) |
| `timestep_hours` | number | no | `1.0` | Δt per step (hours) |
| `crew_count` | integer | no | `0` | Number of crew members |

Number of steps is computed as `max(1, int(duration_hours / timestep_hours))`.

### `events` Array

Each event object:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `time_hours` | number | **yes** | — | Simulation time when event fires |
| `name` | string | **yes** | — | Event identifier (logged in `events_fired`) |
| `payload` | object | no | `null` | Key-value map; values become `state.flags` as `event.<key>` |

> **Note:** Event `handler` callables are only available when building `SimulationEvent` objects programmatically, not from YAML/JSON.

### `parameters` Object

A flat key-value map passed to every subsystem's `update()` each timestep. Keys are subsystem-specific; unknown keys are ignored.

### `subsystems` Array

List of registered subsystem names. If omitted, all built-in subsystems run in registration order:

- `power`
- `eclss`
- `thermal`
- `structure`
- `isru`
- `compute`

Custom plugins registered via `@register_subsystem` can be included by name.

## Built-In Subsystems & Common Parameters

### Power (`power`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `solar_array_kw` | `50.0` | Installed solar capacity |
| `solar_capacity_factor` | `0.25` | Effective capacity factor |
| `battery_kwh` | `200.0` | Battery storage limit |
| `base_load_kw` | `15.0` | Baseline load (+ 0.5 kW per crew) |

### ECLSS (`eclss`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `o2_kg_per_person_day` | `0.84` | O₂ consumption per person-day |
| `water_kg_per_person_day` | `3.0` | Water use per person-day |
| `water_recovery_rate` | `0.93` | Fraction of water recycled |
| `food_kg_per_person_day` | `1.8` | Food mass per person-day |
| `waste_kg_per_person_day` | `0.5` | Waste per person-day |
| `waste_recovery_rate` | `0.75` | Waste processing fraction |
| `eclss_power_kw` | `3.0` | ECLSS electrical load |

### Thermal (`thermal`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ambient_temp_c` | `-20.0` | External temperature |
| `internal_target_c` | `22.0` | Habitat setpoint |
| `internal_heat_kw` | `5.0` | Fixed internal heat (+ 0.1 kW per crew) |
| `radiator_efficiency` | `0.85` | Heat rejection efficiency |

### Structure (`structure`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `pressurized_volume_m3` | `100.0` | Habitable volume |
| `hull_mass_kg` | `8000.0` | Structural mass |
| `radiation_shield_kg` | `12000.0` | Shielding mass |
| `micrometeoroid_annual_risk` | `0.001` | Annual impact risk |
| `max_crew` | `6` | Design crew capacity |

### ISRU (`isru`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `regolith_throughput_kg_h` | `50.0` | Processing rate |
| `o2_extraction_yield` | `0.02` | O₂ yield fraction |
| `water_extraction_yield` | `0.005` | Water yield fraction |
| `isru_power_kw` | `10.0` | ISRU electrical load |

### Compute (`compute`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `compute_nodes` | `4` | Number of compute nodes |
| `watts_per_node` | `150.0` | Power per node |
| `ai_utilization` | `0.4` | AI workload fraction |
| `inference_jobs_per_hour` | `100.0` | Job throughput |
| `radiation_sv_per_year` | `0.3` | Annual radiation dose (Sv) |
| `compute_shielding_factor` | `0.8` | Dose reduction factor |

## Example Snippets

### Minimal YAML

```yaml
name: Quick Test
location: lunar

simulation:
  duration_hours: 24
  timestep_hours: 6
  crew_count: 2

parameters:
  solar_array_kw: 40
  base_load_kw: 10
```

### Events

```yaml
events:
  - time_hours: 168
    name: crew_rotation
    payload:
      alert: 1
  - time_hours: 336
    name: isru_ramp_up
    payload:
      boost: 1
```

When `crew_rotation` fires at hour 168, `state.flags["event.alert"]` is set to `True`.

### Subsystem Selection

Run only power and ECLSS:

```yaml
subsystems:
  - power
  - eclss

simulation:
  duration_hours: 48
  timestep_hours: 12
  crew_count: 4

parameters:
  solar_array_kw: 60
  water_recovery_rate: 0.95
```

### JSON Equivalent

```json
{
  "name": "Lunar Base Alpha",
  "location": "lunar",
  "simulation": {
    "duration_hours": 720,
    "timestep_hours": 6,
    "crew_count": 4
  },
  "events": [
    { "time_hours": 168, "name": "crew_rotation", "payload": { "alert": 1 } }
  ],
  "parameters": {
    "solar_array_kw": 80,
    "solar_capacity_factor": 0.28,
    "battery_kwh": 400
  }
}
```

### Programmatic Config

```python
from astrosim.engine.events import SimulationEvent
from astrosim.engine.state import SimulationConfig
from astrosim.engine.simulator import Simulator
from astrosim.subsystems import DEFAULT_SUBSYSTEMS

config = SimulationConfig(
    name="inline",
    duration_hours=72,
    timestep_hours=6,
    crew_count=3,
    location="mars",
    parameters={"solar_array_kw": 100},
    events=[
        SimulationEvent(time_hours=24, name="checkout", payload={"ready": 1}),
    ],
    subsystems=["power", "thermal"],
)

result = Simulator(config, DEFAULT_SUBSYSTEMS).run()
```

## Validation Notes

- `simulation.duration_hours` must be present; zero or negative values produce at least one step.
- Unknown subsystem names raise `KeyError` at build time.
- Event times are matched with floating-point tolerance (`1e-9`); align events to timestep boundaries for predictable firing.
- Parameter values are not type-checked at load time; subsystems use `.get()` with defaults.

## Related Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) — engine and data flow
- [API.md](API.md) — `load_scenario`, `build_simulator`