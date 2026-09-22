#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VISIBILITY="${1:-public}"
REPO_NAME="${2:-auralyn-click}"
DESCRIPTION="Auralyn Click — modern cross-platform auto clicker for Windows and Linux built with Python and Qt 6"

if [ "$VISIBILITY" != "public" ] && [ "$VISIBILITY" != "private" ]; then
  echo "Usage: ./scripts/publish-github.sh [public|private] [repo-name]"
  exit 2
fi

command -v git >/dev/null || { echo "git is missing: sudo apt install git"; exit 1; }
command -v gh >/dev/null || { echo "GitHub CLI is missing: sudo apt install gh"; exit 1; }

gh auth status >/dev/null 2>&1 || {
  echo "You are not logged into GitHub CLI yet. Run: gh auth login"
  exit 1
}

if [ ! -d .git ]; then
  git init -b main
fi

# If this repository has no Git identity yet, derive a local-only identity
# from the already authenticated GitHub CLI account. This does not change the
# user's global Git configuration.
GH_LOGIN="$(gh api user -q .login)"
GH_ID="$(gh api user -q .id)"
if ! git config user.name >/dev/null; then
  git config user.name "$GH_LOGIN"
fi
if ! git config user.email >/dev/null; then
  git config user.email "${GH_ID}+${GH_LOGIN}@users.noreply.github.com"
fi

VERSION="$(PYTHONPATH=src python3 -c 'from auralyn_click import __version__; print(__version__)')"

git add .
if ! git diff --cached --quiet; then
  git commit -m "Auralyn Click $VERSION"
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "origin already exists: $(git remote get-url origin)"
  git push -u origin main
  exit 0
fi

if gh repo view "$REPO_NAME" >/dev/null 2>&1; then
  OWNER="$(gh api user -q .login)"
  git remote add origin "https://github.com/$OWNER/$REPO_NAME.git"
  git push -u origin main
else
  if [ "$VISIBILITY" = "public" ]; then
    gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source=. --remote=origin --push
  else
    gh repo create "$REPO_NAME" --private --description "$DESCRIPTION" --source=. --remote=origin --push
  fi
fi

echo "✅ Published to GitHub."
