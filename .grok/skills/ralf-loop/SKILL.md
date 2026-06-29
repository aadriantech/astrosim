---
name: ralf-loop
description: >
  DEPRECATED — use pdd-plan, tdd-implement, cdd-review, aysu-verify instead.
  See DEPRECATED.md. Do not invoke for new work.
metadata:
  short-description: "Autonomous RALF dev loop for AstroSim"
---

# RALF Loop — AstroSim Autonomous Development

You are executing the **RALF** development methodology on the AstroSim repository:

| Phase | Action |
|-------|--------|
| **R** — Read | Load requirements and the next task acceptance criterion |
| **A** — Act | Make the **smallest** code change that satisfies the criterion |
| **L** — Learn | Run verification (`pytest` or `py_compile`) |
| **F** — Feedback | Mark the task ✅ in `references/TASKS.md` and report results |

**One task ID per iteration.** Do not batch unrelated changes.

---

## Trigger Phrases

Activate this skill when the user invokes any of:

- `ralf loop` / `ralph loop`
- `/ralf-loop`
- `next task`
- `autonomous loop`
- `continue ralf`

---

## Repository Paths

| Resource | Path |
|----------|------|
| Task tracker | `.grok/skills/ralf-loop/references/TASKS.md` |
| Product requirements | `docs/PRD.md` |
| System requirements | `docs/SRD.md` |
| Source | `src/astrosim/` |
| Tests | `tests/` |
| Scenarios | `scenarios/` |
| Examples | `examples/` |

Always use absolute paths rooted at the AstroSim repo (e.g. `/home/adrianlos/projects/astrosim/...`).

---

## Iteration Protocol

### Step 0 — Orient (every iteration)

1. Read `docs/SRD.md` and `docs/PRD.md` in full (or re-read if already in context this session).
2. Read `.grok/skills/ralf-loop/references/TASKS.md`.
3. Confirm you understand MVP scope: modular subsystems, time-stepped engine, budgeting, AI hooks, visualization, YAML/JSON scenarios.

### Step 1 — Select Next Task

Scan `TASKS.md` for the **first ⬜** following this strict work order:

```
1.4.3.x  →  1.5.3.x  →  1.3.2.x  →  Phase 2  →  Phase 3  →  Phase 4
```

**Selection rules:**

- Within a group (e.g. `1.4.3.x`), pick the lowest incomplete ID (`1.4.3.1` before `1.4.3.2`).
- Skip ✅ tasks.
- If a task is ⬜ but its acceptance criterion is already satisfied in code, mark it ✅ and advance (do not re-implement).
- If blocked, note the blocker and pick the next eligible ⬜ in the same priority band; only escalate to the user if no ⬜ is actionable.

### Step 2 — R: Read Acceptance Criterion

For the selected task ID:

1. Read the **Acceptance** column in `TASKS.md`.
2. Grep/read the files implicated by that criterion.
3. If a test file exists for the task, read it **before** writing code — tests define the contract.
4. State the task ID, acceptance criterion, and planned minimal change.

### Step 3 — A: Act (Minimal Change)

Implement **only** what the acceptance criterion requires:

- Prefer editing existing modules over creating new files.
- Do not refactor unrelated code.
- Do not add features outside the current task ID.
- Match existing code style (dataclasses, type hints, docstrings).
- New tests belong in Phase 2 tasks unless the current task's acceptance explicitly requires a test file.

**Common touch points by area:**

| Area | Typical files |
|------|---------------|
| Subsystems | `src/astrosim/subsystems/*.py` |
| Engine | `src/astrosim/engine/*.py` |
| Budgeting | `src/astrosim/budgeting/*.py` |
| Analysis | `src/astrosim/analysis/*.py` |
| Visualization | `src/astrosim/visualization/*.py` |
| CLI / export | `src/astrosim/cli.py`, `src/astrosim/export/formats.py` |
| Scenarios | `scenarios/*.yaml`, `scenarios/*.json` |

### Step 4 — L: Learn (Verify)

Run verification from the repo root:

```bash
cd /home/adrianlos/projects/astrosim
```

**Preferred** — run targeted pytest:

```bash
# If venv available:
.venv/bin/python -m pytest tests/<relevant_test>.py -q

# Otherwise:
PYTHONPATH=src python3 -m pytest tests/<relevant_test>.py -q
```

**Fallback** — if pytest is unavailable:

```bash
python3 -m py_compile src/astrosim/<changed_module>.py
```

**On failure:** fix within the same iteration (still one task ID). Do not mark ✅ until verification passes.

**On success:** optionally run the broader suite:

```bash
PYTHONPATH=src python3 -m pytest tests/ -q
```

### Step 5 — F: Feedback (Update Tracker)

1. In `references/TASKS.md`, change the completed task's status from ⬜ to ✅.
2. Update the **Quick Reference** section at the bottom:
   - Set **Next incomplete** to the following ⬜ in work order.
   - Update **Verify command** for the new next task.
3. Report to the user:

```
RALF cycle complete
  Task:    <id>
  Change:  <1-line summary>
  Verify:  <command> → PASS
  Next:    <next-id> — <brief description>
```

### Step 6 — Continue or Stop

- If the user said **"ralf loop"** / **"autonomous loop"** (open-ended): immediately start the next iteration from Step 0 without waiting.
- If the user said **"next task"** (single step): stop after one cycle and wait.
- If all tasks are ✅: report MVP complete and suggest Phase 4 release tasks or user review.

---

## Task ID Format

Four-level IDs: `phase.section.subsection.step`

| Phase | Scope |
|-------|-------|
| **1.x** | MVP core — engine, subsystems, budgeting, UI |
| **2.x** | Test coverage (TDD) |
| **3.x** | Examples, CLI polish, coverage gate |
| **4.x** | Release readiness — CI, docs, changelog |

Priority bands for Phase 1 remainder:

| Band | Focus |
|------|-------|
| `1.4.3.x` | Reliability budget — cumulative micrometeoroid risk |
| `1.5.3.x` | Visualization enhancements — web dashboard charts |
| `1.3.2.x` | ECLSS completeness (mostly done; verify & close) |

---

## Guardrails

1. **SRD/PRD are authoritative** — if a task and SRD conflict, SRD wins; note the discrepancy.
2. **One ID per cycle** — never combine `1.4.3.2` and `1.5.3.5` in one iteration.
3. **Tests must pass** before marking ✅.
4. **No scope creep** — no 3D rendering, no CFD, no hardware-in-the-loop (PRD non-goals).
5. **Dependencies stay minimal** — numpy, scipy, pandas, matplotlib, pyyaml only.
6. **Do not delete or rewrite TASKS.md** — only flip ⬜ → ✅ and update Quick Reference.
7. **Preserve MIT license** and existing public API unless the task requires otherwise.

---

## Verification Quick Reference

| Task area | Test file |
|-----------|-----------|
| Structure / 1.4.3.x | `tests/test_structure.py` |
| ECLSS / 1.3.2.x | `tests/test_eclss.py` |
| Web dashboard / 1.5.3.x | `tests/test_srd_features.py` (`test_web_dashboard_generation`) |
| Mass budget / 2.1.1.x | `tests/test_mass_budget.py` |
| Reliability / 2.1.1.x | `tests/test_reliability_budget.py` |
| Export / 2.2.1.x | `tests/test_export.py` |
| CLI / 2.2.1.x | `tests/test_cli.py` |
| Monte Carlo / 2.5.1.x | `tests/test_monte_carlo.py` |
| AI hooks / 2.5.1.x | `tests/test_ai_hooks.py` |
| Full suite / 4.4.1.x | `tests/` |

---

## Example Cycle (1.4.3.2)

```
R: Task 1.4.3.2 — Structure must output micrometeoroid_cumulative_risk
   Read tests/test_structure.py → expects cumulative > step risk

A: Edit src/astrosim/subsystems/structure.py
   Track cumulative risk in _local_state, return in outputs dict

L: PYTHONPATH=src python3 -m pytest tests/test_structure.py -q

F: Mark 1.4.3.2 ✅, set Next incomplete → 1.5.3.5
```

---

## Autonomous Loop Pseudocode

```
loop:
    read SRD.md, PRD.md, TASKS.md
    task = first_incomplete_by_work_order()
    if task is None: report done; break

    read acceptance criterion for task
    implement minimal fix
    run pytest or py_compile
    if fail: fix and re-run (same task)
    mark task ✅ in TASKS.md
    report cycle summary
    if single-shot: break
```

---

## Installing Test Dependencies

If pytest is missing:

```bash
cd /home/adrianlos/projects/astrosim
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest tests/ -q
```

Use this once per environment; subsequent cycles use `.venv/bin/python -m pytest`.