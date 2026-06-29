# Release Process

## Prerequisites

- All Phase exit tests green locally: `bash scripts/integrity_check.sh`
- `CHANGELOG.md` updated for the target version

## Push to GitHub

```bash
cd /home/adrianlos/projects/astrosim
git push -u origin main
```

Requires GitHub credentials (PAT or SSH). CI must pass on `main`.

## Tag a release

```bash
git tag -a v0.1.0 -m "AstroSim MVP"
git push origin v0.1.0
```

Pushing a `v*` tag triggers `.github/workflows/release.yml` (GitHub Release notes).

## Verify remote CI

1. Open https://github.com/aadriantech/astrosim/actions
2. Confirm latest `CI` workflow is green
3. Confirm `Release` workflow completed for the tag

## PyPI (optional, Phase 6.7)

See `.github/workflows/publish.yml` — manual `workflow_dispatch` with `PYPI_API_TOKEN` secret.