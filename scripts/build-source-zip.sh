#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(PYTHONPATH="$ROOT/src" python3 -c 'from auralyn_click import __version__; print(__version__)')"
OUT="${1:-$ROOT/../AuralynClick-$VERSION-GitHub-Source.zip}"
cd "$(dirname "$ROOT")"
rm -f "$OUT"
zip -r "$OUT" "$(basename "$ROOT")" \
  -x '*/.git/*' '*/.venv/*' '*/__pycache__/*' '*.pyc' '*/build/*' '*/dist/*' '*/release/*'
echo "Created: $OUT"
