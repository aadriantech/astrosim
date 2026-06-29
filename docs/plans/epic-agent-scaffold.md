---
task_id: epic-agent-scaffold
task_class: T3
status: ready
epic: agent-infrastructure
srd_refs: ["§3", "§4"]
approver: grok-architect
---

# PDD: Agent Infrastructure & Distributed Memory

## Problem

Establish PDD→TDD→CDD→AYSU discipline and indexed section memory before further feature work.

## Deliverables

1. `AGENTS.md` + `AGENT_INDEX.md`
2. Section `AGENT.md` per domain (baseline audit, VERIFIED/UNVERIFIED)
3. Skills: pdd-plan, tdd-implement, cdd-review, aysu-verify, memory-sync
4. `contracts/critic_review.schema.md`
5. Deprecate ralf-loop
6. `scripts/check_agent_sync.sh`

## Acceptance criteria

1. [x] All AGENT_INDEX paths exist
2. [x] `check_agent_sync.sh` exits 0
3. [x] CONTRIBUTING references new methodology
4. [x] No new application feature code in this epic

## Out of scope

- JSON Schema contracts (next epic: epic-contracts)
- GitHub repo creation

## CDD focus areas

Methodology collision with RALF; enforceability of AYSU; memory accuracy.