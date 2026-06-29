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

**Option B — SSH (recommended on this host):**

Remote uses `git@github.com-aadriantech:aadriantech/astrosim.git` with key `~/.ssh/id_ed25519_aadriantech`.

```bash
git push -u origin main
git push origin v0.3.0
```

Restore CI workflows after scope refresh:

```bash
gh auth refresh -h github.com -s workflow,repo
bash scripts/restore_ci_push.sh
```

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

## PyPI (Phase 9.1)

1. Create API token at https://pypi.org/manage/account/token/ (scope: entire account or project `astrosim`).
2. Add GitHub repository secret `PYPI_API_TOKEN` (Settings → Secrets → Actions).
3. Trigger publish workflow:

```bash
gh workflow run publish.yml --repo aadriantech/astrosim
```

4. Verify install:

```bash
python3 -m venv /tmp/astrosim-pypi-test
/tmp/astrosim-pypi-test/bin/pip install astrosim==0.5.0
/tmp/astrosim-pypi-test/bin/astrosim --help
```

**TestPyPI fallback** (no production token):

```bash
pip install build twine
python3 -m build
TWINE_USERNAME=__token__ TWINE_PASSWORD=<testpypi-token> \
  twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple/ astrosim==0.5.0
```

If `PYPI_API_TOKEN` is not set, Phase 9 exit gate accepts TestPyPI proof documented in release notes.

## GitHub Pages (Phase 12)

1. Repo **Settings → Pages → Build and deployment → GitHub Actions**
2. Push to `main` runs `.github/workflows/docs.yml`
3. MkDocs site builds from `mkdocs.yml`; deploy step requires Pages enabled on the repo