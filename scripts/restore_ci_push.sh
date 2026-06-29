#!/usr/bin/env bash
# Restore .github/workflows and push after workflow scope is granted.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .github/workflows ]]; then
  echo "ERROR: .github/workflows missing"
  exit 1
fi

echo "Ensure workflow scope: gh auth refresh -h github.com -s workflow,repo"
/home/adrianlos/.local/bin/gh auth setup-git 2>/dev/null || true

git add .github/workflows
git diff --cached --quiet && echo "Workflows already committed" || \
  git commit -m "ci: restore GitHub Actions workflows"

git push origin main
echo "CI workflows pushed. Check https://github.com/aadriantech/astrosim/actions"