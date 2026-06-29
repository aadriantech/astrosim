# Release Process

## Prerequisites

- All Phase exit tests green locally: `bash scripts/integrity_check.sh`
- `CHANGELOG.md` updated for the target version

## Push to GitHub

**Option A — automated script (recommended):**

```bash
# 1. Authenticate (one-time): visit https://github.com/login/device with code from:
~/.local/bin/gh auth login --hostname github.com --git-protocol ssh --skip-ssh-key -p ssh

# Or set a PAT: export GITHUB_TOKEN=ghp_...

# 2. Push (creates repo if missing):
cd /home/adrianlos/projects/astrosim
bash scripts/push_github.sh
```

**Option B — manual:** Create empty repo `aadriantech/astrosim` on GitHub, then:

```bash
git push -u origin main
git push origin v0.1.0 v0.2.0
```

SSH auth on this host is configured for `icgtdistrictlos`. You need repo create access under `aadriantech` or set `GITHUB_OWNER=icgtdistrictlos`.

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