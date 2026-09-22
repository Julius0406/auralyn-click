#!/usr/bin/env bash
set -euo pipefail
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  VERSION="$(PYTHONPATH=src python3 -c 'from auralyn_click import __version__; print(__version__)')"
fi
TAG="v$VERSION"
if ! command -v git >/dev/null; then echo "git is required"; exit 1; fi
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree has uncommitted changes. Commit them first."
  exit 1
fi
git tag -a "$TAG" -m "Auralyn Click $VERSION"
git push origin "$TAG"
echo "Pushed $TAG. GitHub Actions will build Linux and Windows installers and create the Release."
