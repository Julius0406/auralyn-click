#!/usr/bin/env bash
set -euo pipefail

APP_SLUG="auralyn-click"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$HOME/.local/share/$APP_SLUG"
BIN="$HOME/.local/bin"

if [ ! -d "$DEST" ] || [ ! -x "$DEST/.venv/bin/python" ]; then
  echo "No existing Auralyn Click installation found — running the full installer."
  exec "$ROOT/scripts/install.sh"
fi

if [ -x "$BIN/auralyn-click-control" ]; then
  "$BIN/auralyn-click-control" stop 2>/dev/null || true
fi
pkill -f "$DEST/src/auralyn_click" 2>/dev/null || true
sleep 0.2

mkdir -p "$DEST"
rm -rf "$DEST/src"
cp -r "$ROOT/src" "$DEST/src"
rm -rf "$DEST/assets"
cp -r "$ROOT/assets" "$DEST/assets"
cp "$ROOT/requirements.txt" "$DEST/requirements.txt"
cp "$ROOT/LICENSE" "$DEST/LICENSE"

"$DEST/.venv/bin/python" -m pip install -r "$DEST/requirements.txt"

# Keep helper/launcher current as well.
cp "$ROOT/auralyn-click-control.py" "$BIN/auralyn-click-control"
chmod +x "$BIN/auralyn-click-control"

cat > "$BIN/auralyn-click" <<EOF
#!/usr/bin/env bash
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_ENABLE_HIGHDPI_SCALING=1
export PYTHONPATH="$DEST/src"
exec "$DEST/.venv/bin/python" -m auralyn_click "\$@"
EOF
chmod +x "$BIN/auralyn-click"

echo "✅ Auralyn Click updated without resetting your settings."
nohup "$BIN/auralyn-click" >/dev/null 2>&1 &
