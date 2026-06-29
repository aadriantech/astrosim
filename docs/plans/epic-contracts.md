---
task_id: epic-contracts
task_class: T2
status: complete
epic: contracts
srd_refs: ["§4"]
approver: grok-architect
---

# PDD: Interface Contracts

## Problem

SRD §4 requires YAML/JSON configuration and clear subsystem APIs. Contracts are ad-hoc; `lunar_base.json` diverges from YAML.

## Architect decisions

| Topic | Decision |
|-------|----------|
| Schema format | JSON Schema draft 2020-12 for scenarios + export (export deferred) |
| Validation lib | `jsonschema` in `[dev]` only |
| Subsystem contract | YAML manifest of required output keys per subsystem |
| Events | Catalog with `handler: active \| noop` — documents current behavior |
| Parity rule | Lunar JSON must have **same parameter keys** as YAML; values match |

## Interfaces

- `contracts/scenario.schema.json`
- `contracts/subsystem_outputs.yaml`
- `contracts/events.yaml`

## Edge cases

1. Scenario missing optional `description` — valid
2. Event with empty payload — valid; noop handler
3. Unknown event name — allowed in schema; catalog marks noop
4. Subsystem returns extra keys — allowed; contract tests required keys only

## Acceptance criteria

1. [x] `scenario.schema.json` validates `lunar_base.yaml` and `lunar_base.json` (via parsed dict)
2. [x] `subsystem_outputs.yaml` lists required keys; tests assert each subsystem produces them
3. [x] `events.yaml` catalogs all scenario events with handler semantics
4. [x] `tests/test_contracts_*.py` cover schema, outputs, events, parity
5. [x] `lunar_base.json` parameter keys + values match YAML

## Architect Q&A (resolved)

| Question | Decision |
|----------|----------|
| export_result.schema.json | Follow-up epic `epic-export-contract` |
| Uncataloged events | Permissive schema; catalog test ensures scenario events ⊆ catalog |
| Parity scope | Parameters only for v1; full dict parity deferred |
| `subsystems` in schema | In-scope — matches `SimulationConfig.subsystems` |

## Out of scope

- `export_result.schema.json` (follow-up)
- New event handler implementations
- Physics changes

## CDD focus

Schema too strict/loose; parity test brittleness; jsonschema dep addition.