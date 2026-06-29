---
task_id: epic-release-prep
task_class: T3
status: complete
epic: release-prep
srd_refs: ["§2", "§4"]
approver: grok-architect
---

# PDD: Release Prep & Hardening

## Problem

MVP is feature-complete with contracts, but CI lacks coverage/example gates, registry tests pollute global state, `scipy` is unused, and the repo has no initial commit on GitHub.

## Architect decisions

| Topic | Decision |
|-------|----------|
| Coverage gate | `--cov=astrosim --cov-fail-under=80` in CI (current: 82%) |
| Example smoke | `scripts/smoke_examples.sh` runs `run_lunar_base.py`, asserts output files |
| Registry cleanup | Add `unregister_subsystem()`; tests must clean up plugins |
| scipy | Remove from `dependencies` — unused in `src/` |
| Git push | Initial commit to `main`; fix malformed remote URL |

## Interfaces

- `unregister_subsystem(name: str) -> None` in `registry.py`
- `scripts/smoke_examples.sh` (new)

## Edge cases

1. `unregister_subsystem` on unknown name — no-op
2. Smoke script must not require network or LLM
3. Coverage gate may fail if `cli.py` excluded — use package-level cov only

## Acceptance criteria

1. [x] CI runs pytest with `--cov-fail-under=80`
2. [x] CI runs `scripts/smoke_examples.sh`
3. [x] `unregister_subsystem` exported; `test_custom_subsystem_plugin` cleans up
4. [x] Test asserts builtin count stable after plugin test
5. [x] `scipy` removed from `pyproject.toml`
6. [x] All pytest green; smoke script passes locally
7. [x] Initial git commit pushed to `origin/main` (if remote accessible)

## Out of scope

- scipy.optimize sensitivity (future epic)
- Full example suite in CI (mars MC too slow)
- Coverage gate on `cli.py` subprocess path

## CDD focus

Registry API misuse; smoke script side effects; CI runtime on prod host during dev.