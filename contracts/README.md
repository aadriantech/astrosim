# Contracts (CDD)

**Canonical source** for interfaces. Section `AGENT.md` files link here — they do not duplicate field lists.

| File | Purpose | Status |
|------|---------|--------|
| [critic_review.schema.md](critic_review.schema.md) | CDD review output format | active |
| [scenario.schema.json](scenario.schema.json) | Scenario YAML/JSON validation | active |
| [subsystem_outputs.yaml](subsystem_outputs.yaml) | Required output keys per subsystem | active |
| [events.yaml](events.yaml) | Event catalog + semantics | active |
| [export_result.schema.json](export_result.schema.json) | Simulation export JSON shape | active |
| [optimization_result.schema.json](optimization_result.schema.json) | Optimizer output from `minimize_metric` | active |
| [llm_insight.schema.json](llm_insight.schema.json) | Structured LLM insight response | active |
| [trade_study.schema.json](trade_study.schema.json) | Pareto trade study export | active |
| [study_report.schema.json](study_report.schema.json) | Study report metadata sidecar | planned (Phase 9) |
| [scenario_compare.schema.json](scenario_compare.schema.json) | Multi-scenario compare export | planned (Phase 9) |

New interfaces: update contract first (PDD), then tests (TDD), then code.

**Note:** `events.yaml` `handler` documents runtime behavior in `apply_event_payload`; behavioral guardrails in `tests/test_contracts_events.py`.