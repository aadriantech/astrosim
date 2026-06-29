# Plugin Cookbook

## Register a custom subsystem

```python
from astrosim.subsystems import Subsystem, register_subsystem, unregister_subsystem

@register_subsystem
class GreenhouseSubsystem(Subsystem):
    name = "greenhouse"

    def update(self, state, dt_hours, params):
        rate = params.get("growth_rate_kg_per_hour", 0.05)
        biomass = self._local_state.get("biomass_kg", 0.0) + rate * dt_hours
        return {"biomass_kg": biomass, "growth_kg": rate * dt_hours}

# Run simulation with subsystems=["power", "greenhouse"]
```

## Clean up after tests or scripts

Always unregister plugins you add in tests:

```python
try:
    ...  # test or demo
finally:
    unregister_subsystem("greenhouse")
```

See `examples/custom_subsystem.py` and `tests/test_srd_features.py`.

## Scenario filter

```yaml
simulation:
  duration_hours: 48
  timestep_hours: 12
  crew_count: 2
subsystems:
  - power
  - greenhouse
```

Omit `subsystems` to run all built-in registered modules.