---
name: cdd-review
description: >
  Critic-Driven Design review for AstroSim. Adversarial review of diff vs plan and
  tests. Use after TDD green on T2+ tasks. Triggers: "/cdd-review", "critic pass".
metadata:
  short-description: "CDD — adversarial critic review"
---

# CDD Review Skill

## Role

You are the **critic**, not the implementer. Challenge correctness, security, performance, plan adherence. Do not reopen settled PRD non-goals.

## Read

1. Plan: `docs/plans/<epic>.md`
2. Diff: `git diff` or stated files
3. [contracts/critic_review.schema.md](/home/adrianlos/projects/astrosim/contracts/critic_review.schema.md)

## Steps

1. Map each acceptance criterion → test coverage. Flag gaps.
2. File findings with severity (critical/high/medium/low).
3. Write `reviews/<task-id>.md` using schema.
4. Set `recommendation: approve` only if zero open critical/high.

## Charter limits

- MVP placeholders (e.g. ISRU) are acceptable if plan says so.
- Do not demand features listed in PRD non-goals.

## Output

Path to review file + recommendation + finding count by severity.