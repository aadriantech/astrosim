---
task_id: epic-event-handlers
task_class: T2
status: complete
epic: event-handlers
srd_refs: ["§2.1"]
approver: grok-architect
---

# PDD: Active Event Handlers

## Problem

`dust_storm` and `crew_rotation` are cataloged as noop but fire in Mars/lunar scenarios. MVP event-driven sim should mutate config meaningfully.

## Architect decisions

| Event | Behavior |
|-------|----------|
| `dust_storm` | Reduce `solar_capacity_factor` by `0.5 * severity`; severity from `severity` or `alert` (default 0.3); set `dust_storm_active` |
| `crew_rotation` | Set `crew_rotation_active`; bump `water_recovery_rate` by +0.02 (cap 0.99) |

## Acceptance criteria

1. [x] Handlers in `apply_event_payload`
2. [x] `contracts/events.yaml` updated to `handler: active`
3. [x] Behavioral tests replace noop crew_rotation test
4. [x] Integration test: dust_storm reduces power generation in sim

## Out of scope

- Timed recovery from dust storm; crew count changes