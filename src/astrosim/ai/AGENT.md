# AGENT — AI Hooks

**Scope:** LLM integration + offline optimization heuristics.  
**Owns:** `ai/*.py`  
**Depends on:** ENG  
**Last verified:** 2026-06-29 · baseline audit

## Purpose

`AIHooks` builds context from results; optional `LLMClient` for insights. Offline fallbacks always available.

## Gotchas

- `adapters.py` network paths lightly tested — mock in CI only when added.
- Never call live LLM in pytest CI.

## Verification status

| Claim | Status |
|-------|--------|
| Offline insights non-empty | VERIFIED |
| Solar suggestion on energy deficit | VERIFIED |
| Water recovery on mass import | VERIFIED |

## Tests

- `tests/test_ai_hooks.py`