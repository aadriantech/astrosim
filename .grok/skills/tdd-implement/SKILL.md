---
name: tdd-implement
description: >
  Test-Driven implementation for AstroSim. Use after PDD plan is ready, or for T0
  trivial fixes. Triggers: "/tdd-implement", "implement plan", "make tests pass".
metadata:
  short-description: "TDD — tests first, then code"
---

# TDD Implement Skill

## Preconditions

- T1+: `docs/plans/<epic>.md` exists with `status: ready`
- Section AGENT.md loaded per AGENT_INDEX

## Steps

1. Read plan acceptance criteria.
2. **Assert:** write failing test(s) in `tests/`.
3. Run `PYTHONPATH=src pytest <new tests> -q` — confirm FAIL for right reason.
4. **Launch:** minimal `src/` change to green.
5. Run full `pytest tests/ -q`.
6. If behavior changed, update section AGENT.md §Verification status.

## Must not

- Expand beyond plan scope
- Skip failing-test step
- Fix tests to match wrong implementation without plan update

## Output

Diff summary + pytest result + tests added.