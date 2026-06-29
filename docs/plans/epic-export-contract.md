---
task_id: epic-export-contract
task_class: T2
status: complete
epic: export-contract
srd_refs: ["§4"]
approver: grok-architect
---

# PDD: Export Result Contract

## Problem

`export_json()` produces a stable JSON shape (config, budgets, history) but there is no canonical schema. CDD cannot validate export compatibility across releases. Deferred from `epic-contracts`.

## Architect decisions

| Topic | Decision |
|-------|----------|
| Schema format | JSON Schema draft 2020-12, mirrors `export_json()` payload |
| Validation lib | `jsonschema` in `[dev]` (already present) |
| Budget sections | `oneOf`: empty `{}` (no budget) or full summary keys |
| Reliability extras | `patternProperties` for `risk_<subsystem>` keys |
| History rows | Require `time_hours`, `step`, `mass_kg`, reliability derived fields; allow extra numeric metric keys |
| Code changes | None expected — contract documents existing `formats.export_json` |

## Interfaces

- `contracts/export_result.schema.json` (new)
- `tests/test_contracts_export.py` (new)

## Edge cases

1. Budget `None` → export emits `{}` — valid
2. Empty `history` array — valid (zero-step edge)
3. Dynamic `risk_*` keys in reliability summary — valid via pattern
4. History row with extra subsystem metrics — valid; only core keys required

## Acceptance criteria

1. [x] `export_result.schema.json` exists and uses draft 2020-12
2. [x] Live `export_json()` output from short simulation validates against schema
3. [x] Minimal hand-crafted payloads (empty budgets, empty history) validate
4. [x] Invalid payload missing required top-level key fails validation
5. [x] `contracts/README.md` marks export schema `active`
6. [x] `tests/test_contracts_export.py` covers criteria 2–4

## Out of scope

- CSV export schema
- Changing `export_json()` structure
- `export_result` versioning field

## CDD focus

Schema too strict on history metrics; empty-budget oneOf; no false negatives on real exports.