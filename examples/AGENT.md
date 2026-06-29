# AGENT — Examples

**Scope:** Runnable demos; `run_lunar_base.py` CI-smoked.  
**Owns:** `examples/*.py`  
**Depends on:** PKG, SCE  
**Last verified:** 2026-06-28

## Scripts

| Script | Shows |
|--------|-------|
| `run_lunar_base.py` | Full export + dashboards |
| `run_mars_habitat.py` | Monte Carlo |
| `run_sensitivity.py` | OAT sensitivity |
| `custom_subsystem.py` | Plugin pattern |

## CI

- `scripts/smoke_examples.sh` runs `run_lunar_base.py` and checks `output/lunar_base/*`