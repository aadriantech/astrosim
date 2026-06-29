# AstroSim — Agent Operating Manual

**Authority:** Tech architect decisions (Adrian delegated).  
**Scope:** How agents work in this repo. Domain knowledge lives in section `AGENT.md` files — not here.

## Methodology (strict order)

| Step | Name | Artifact | Gate |
|------|------|----------|------|
| 1 | **PDD** | `docs/plans/<epic>.md` | Plan complete; acceptance criteria numbered |
| 2 | **TDD** | `tests/` | Failing test first → green → refactor |
| 3 | **CDD** | `reviews/<task-id>.md` | 0 open critical/high findings |
| 4 | **AYSU** | PR / session summary | Structured block; confidence = high |

**No plan → no code. No green tests → no CDD. No CDD approve → no AYSU. AYSU not high → loop back.**

Invoke skills: `/pdd-plan` → `/tdd-implement` → `/cdd-review` → `/aysu-verify`

## Task classes

| Class | When | Pipeline |
|-------|------|----------|
| **T0** | Typo, comment, pure docs | TDD (if tests touched) → AYSU |
| **T1** | Single module, clear SRD ref | Light PDD → TDD → AYSU |
| **T2** | Cross-module, API, contracts | Full PDD → TDD → CDD → AYSU |
| **T3** | Release, CI, architecture | Full pipeline + human sign-off |

Default unknown tasks to **T2**.

## Memory read protocol

1. Read **`AGENT_INDEX.md`** (domain routing).
2. Read **this file** if new session or methodology unclear.
3. Load **primary** section `AGENT.md` (+ up to **2 secondary** per index).
4. Load **`contracts/`** only when touching interfaces or schemas.
5. **Never** load all section files in one session.

## Sub-agents

| Role | Skill | Produces | Must not |
|------|-------|----------|----------|
| Planner | `pdd-plan` | `docs/plans/<epic>.md` | Code, tests |
| Implementer | `tdd-implement` | `src/` + `tests/` | Skip tests, expand scope |
| Critic | `cdd-review` | `reviews/<id>.md` | Implement fixes |
| Verifier | `aysu-verify` | AYSU block | Ship on low confidence |

**Handoff:** Planner → Implementer → Critic → Verifier. Any gate fails → previous role.

## Stack conventions

- Python ≥3.10, `src/astrosim/` layout, hatchling, pytest
- Type hints on public APIs; docstrings on modules/classes
- MIT license; minimal deps (numpy, pandas, matplotlib, pyyaml)
- Fix `src/`, not tests, when requirement is stable

## AYSU checklist (required before done)

```
AYSU:
  confidence: high | medium | low
  task_class: T0 | T1 | T2 | T3
  verified:
    - [ ] Plan acceptance criteria met
    - [ ] pytest green
    - [ ] Critic approve (T2+)
    - [ ] Section AGENT.md updated if behavior changed
  residual_risks: <list or "none">
  loop_back: no
```

## Deprecated

**RALF loop** (`.grok/skills/ralf-loop`) is retired. Use PDD→TDD→CDD→AYSU. See `.grok/skills/ralf-loop/DEPRECATED.md`. Decision record: [ai-coding-scaffold/docs/DECISIONS.md](https://github.com/aadriantech/ai-coding-scaffold/blob/main/docs/DECISIONS.md).

## Related

- Index: [AGENT_INDEX.md](AGENT_INDEX.md)
- Contributing: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)
- Section template: [docs/AGENT_TEMPLATE.md](docs/AGENT_TEMPLATE.md)