---
task_id: epic-phase16
task_class: T2
status: ready
epic: reference-validation-interpretation-v2
srd_refs: ["§2.2", "§2.3", "§2.4"]
approver: pending
target_version: "1.2.0"
---

# PDD: Phase 16 — Reference Validation & Interpretation v2

## Problem

Outputs now include implications and verdicts, but lack traceability to official NASA/public
baselines and no automated accuracy gate. Users cannot tell whether AstroSim parameters and
results align with BVAD/OCHMO/ISS envelopes. Interpretation also omits structured actions and
reference citations.

Links: PRD §7 (public data), SRD §2.2–2.3 (subsystems, analysis).

## Interfaces

| Artifact | Change |
|----------|--------|
| `reference/benchmarks.yaml` | New — curated official reference values + scenario envelopes |
| `src/astrosim/validation/` | New — `load_benchmarks`, `validate_result`, `format_validation_table` |
| `contracts/validation_report.schema.json` | New — validation JSON shape |
| `contracts/study_report.schema.json` | Add optional `actions`, `references`, `validation` |
| `src/astrosim/export/interpretation.py` | Add `actions`, `references` on `ResultInterpretation` |
| `src/astrosim/export/study_report.py` | Sections: References, Recommended Actions, Validation |
| `src/astrosim/cli.py` | `--validate` flag → `validation_report.json` + stdout table |

## Edge cases

1. Scenario without named envelope — run parameter + derived checks only.
2. Missing benchmark file — raise clear `FileNotFoundError` with default path hint.
3. Zero crew or zero duration — skip per-crew-year scaling checks with `warn`.
4. Envelope metric out of range — `warn` (soft), not CI-hard-fail for energy surplus model bias.

## Acceptance criteria

1. [ ] `reference/benchmarks.yaml` documents ECLSS consumables (BVAD/OCHMO) and `orbital_station` envelope.
2. [ ] `validate_result()` returns checks with `pass`/`warn`/`fail` and `overall_status`.
3. [ ] Parameter fidelity test: `o2_kg_per_person_day=0.84` in canonical scenarios passes within tolerance.
4. [ ] Derived-rate test: simulated O₂ kg/person/day matches scenario parameter within 1%.
5. [ ] Envelope test: `orbital_station.yaml` mass import per crew-year passes configured band.
6. [ ] `interpret_result()` populates `actions` and `references`; study report renders new sections.
7. [ ] `study_report.json` validates against updated schema (optional new fields).
8. [ ] CLI `--validate` writes `validation_report.json` and prints summary table; exit 0 on pass/warn.
9. [ ] `contracts/validation_report.schema.json` contract test passes.
10. [ ] Full `pytest tests/ -q` green.

## Out of scope

- Parsing BVAD PDFs automatically
- LLM-generated validation
- Monte Carlo-aware interpretation (deferred Phase 17)
- `docs/VALIDATION.md` (user did not request doc file)

## Implementation notes

- Default benchmarks path: `<repo>/reference/benchmarks.yaml`
- Reuse optimization suggestion logic from `AIHooks.suggest_optimizations` for actions.
- Orbital energy envelope uses wide upper bound — simplified power model over-surplus vs ISS.

## CDD focus areas

- Schema `additionalProperties` consistency
- No circular imports between `validation` and `export`
- CLI exit codes: fail only on `overall_status == "fail"`