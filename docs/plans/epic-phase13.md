---
task_id: epic-phase13
task_class: T2
status: complete
epic: phase13
target_version: "0.9.0"
---

# PDD: Phase 13 — O₂ Closed-Loop & Orbital Biosphere

## Problem

Water and food loops exist; O₂ from ISRU does not credit ECLSS consumption. No orbital greenhouse scenario.

## Work order

```
13.1 ISRU–ECLSS O₂ loop      (T2)
13.2 orbital_greenhouse      (T1)
13.3 closed-loop audit test  (T2)
13.4 Release v0.9.0          (T3)
```

## Acceptance

1. [ ] `o2_supplied_kg`, `o2_net_import_kg` on ECLSS outputs + contract
2. [ ] ISRU before ECLSS lowers net O₂ import
3. [ ] `orbital_greenhouse.yaml` + JSON parity
4. [ ] `tests/test_closed_loop_audit.py` green

## Out of scope

- CO₂ scrubbing chemistry model