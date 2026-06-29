# AGENT — Subsystems

**Scope:** Pluggable habitat models + registry.  
**Owns:** `subsystems/*.py`  
**Depends on:** ENG  
**Last verified:** 2026-06-29 · baseline audit

## Purpose

Six built-ins: power, eclss, thermal, structure, isru, compute. Register custom via `@register_subsystem`.

## Gotchas

- `get_state()` populated via `step()`, not bare `update()`.
- ISRU is **placeholder** fidelity — PRD MVP scope.
- `unregister_subsystem()` cleans up test plugins — **VERIFIED** in `test_custom_subsystem_plugin`.

## Verification status

| Claim | Status |
|-------|--------|
| All six have unit tests | VERIFIED |
| Plugin register + build | VERIFIED |
| Output key contracts | VERIFIED — `contracts/subsystem_outputs.yaml` + `tests/test_contracts_subsystems.py` |

## Tests

- `tests/test_power.py`, `test_eclss.py`, `test_thermal.py`, `test_isru.py`, `test_compute.py`, `test_structure.py`, `test_subsystem_base.py`

## Related

- [budgeting/AGENT.md](../budgeting/AGENT.md)