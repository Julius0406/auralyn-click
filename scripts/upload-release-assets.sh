#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-Julius0406/auralyn-click}"
VERSION="${1:-2.4.4}"
TAG="v$VERSION"
DIR="${2:-$HOME/Downloads}"

command -v gh >/dev/null || { echo "GitHub CLI (gh) is required."; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Run: gh auth login"; exit 1; }

FILES=(
  "$DIR/AuralynClick-$VERSION-GitHub-Source.zip"
  "$DIR/AuralynClick-$VERSION-Windows-Installer-Source.zip"
  "$DIR/AuralynClick-$VERSION-Ubuntu-Debian.deb"
)

for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "Missing: $f"
    exit 1
  fi
done

gh release upload "$TAG" "${FILES[@]}" --repo "$REPO" --clobber

echo "Uploaded release helper assets to $REPO / $TAG"
