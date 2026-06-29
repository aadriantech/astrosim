# AGENT — Scenarios

**Scope:** YAML/JSON mission definitions.  
**Owns:** `scenarios/*`  
**Depends on:** SCE, CON (when schemas land)  
**Last verified:** 2026-06-29 · baseline audit

## Files

- `lunar_base.yaml` — canonical full param set
- `lunar_base.json` — parity with YAML **VERIFIED** (`tests/test_scenario_parity.py`)
- `mars_habitat.yaml` — long-duration Mars; has events

## Gotchas

- Events must be listed in `contracts/events.yaml`. `description` is file metadata only (not loaded into config).
- JSON loader uses same schema as YAML via `config_from_dict`.

## Tests

- `tests/test_scenario.py`, `tests/test_contracts_scenario.py`, `tests/test_contracts_parity.py`