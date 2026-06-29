---
task_id: epic-scenario-parity
task_class: T2
status: complete
epic: scenario-parity
srd_refs: ["§4"]
approver: grok-architect
---

# PDD: Scenario Parity Completion

## Problem

`mars_habitat.json` missing. TASKS `3.1.3.1` pending. Parity tests cover lunar parameters only.

## Acceptance criteria

1. [x] `scenarios/mars_habitat.json` mirrors YAML parameters + events + simulation
2. [x] Parity tests cover mars parameter keys/values
3. [x] Full structural parity test (name, location, simulation, events, parameters) for lunar + mars
4. [x] `test_contracts_scenario.py` validates mars JSON
5. [x] TASKS.md `3.1.3.1` marked complete

## Out of scope

- New scenario content; physics changes