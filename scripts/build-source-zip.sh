#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/../AuralynClick-Source.zip}"
cd "$(dirname "$ROOT")"
rm -f "$OUT"
zip -r "$OUT" "$(basename "$ROOT")" -x '*/.git/*' '*/.venv/*' '*/__pycache__/*' '*.pyc'
echo "Created: $OUT"
