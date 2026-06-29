# AGENT — CI/CD

**Scope:** GitHub Actions, PR/issue templates.  
**Owns:** `.github/**`  
**Depends on:** TST, ROOT  
**Last verified:** 2026-06-29

## Workflows

- `ci.yml` — Python 3.11, `pip install -e ".[dev]"`, coverage gate, example smoke

## Gates

- `scripts/check_agent_sync.sh` in CI
- `pytest --cov=astrosim --cov-fail-under=80`
- `scripts/smoke_examples.sh` (`run_lunar_base.py`)

## PR requirements

- AYSU block in description (see `pull_request_template.md`)
- T2+: link `reviews/<task-id>.md` with approve