#!/usr/bin/env bash
# Create GitHub repo (if needed) and push main + tags.
# Requires one of:
#   - GITHUB_TOKEN env var (repo scope), or
#   - gh auth login (SSH keys used for git push)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OWNER="${GITHUB_OWNER:-aadriantech}"
REPO="${GITHUB_REPO:-astrosim}"
REMOTE="git@github.com:${OWNER}/${REPO}.git"

GH="${GH:-gh}"
if ! command -v "$GH" >/dev/null 2>&1; then
  GH="${HOME}/.local/bin/gh"
fi

git remote set-url origin "$REMOTE"

if [[ -n "${GITHUB_TOKEN:-}" ]] && command -v "$GH" >/dev/null 2>&1; then
  echo "$GITHUB_TOKEN" | "$GH" auth login --with-token 2>/dev/null || true
fi

if command -v "$GH" >/dev/null 2>&1 && "$GH" auth status >/dev/null 2>&1; then
  if ! "$GH" repo view "${OWNER}/${REPO}" >/dev/null 2>&1; then
    echo "Creating ${OWNER}/${REPO}..."
    "$GH" repo create "${OWNER}/${REPO}" --public --description "Open-source space habitat simulation framework"
  fi
fi

echo "Pushing main..."
GIT_SSH_COMMAND="ssh -o BatchMode=yes" git push -u origin main

echo "Pushing tags..."
GIT_SSH_COMMAND="ssh -o BatchMode=yes" git push origin v0.1.0 v0.2.0 2>/dev/null || \
  git push origin --tags

echo "Done: https://github.com/${OWNER}/${REPO}"