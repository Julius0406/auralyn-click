#!/usr/bin/env bash
set -euo pipefail
APP_SLUG="auralyn-click"
APP_NAME="Auralyn Click"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$HOME/.local/share/$APP_SLUG"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/512x512/apps"

printf '\n=== %s Installer ===\n\n' "$APP_NAME"
if command -v apt >/dev/null 2>&1; then
  echo "==> Checking Ubuntu runtime packages..."
  sudo apt update
  sudo apt install -y python3 python3-venv python3-pip libxcb-cursor0
fi

if [ -x "$BIN_DIR/auralyn-click-control" ]; then "$BIN_DIR/auralyn-click-control" stop 2>/dev/null || true; fi
pkill -f "$DEST/src/auralyn_click" 2>/dev/null || true
sleep 0.2
mkdir -p "$DEST" "$BIN_DIR" "$APP_DIR" "$ICON_DIR"
rm -rf "$DEST/src" "$DEST/assets"
cp -r "$ROOT/src" "$DEST/src"
cp -r "$ROOT/assets" "$DEST/assets"
cp "$ROOT/requirements.txt" "$DEST/requirements.txt"
cp "$ROOT/LICENSE" "$DEST/LICENSE"

if [ ! -x "$DEST/.venv/bin/python" ]; then python3 -m venv "$DEST/.venv"; fi
"$DEST/.venv/bin/python" -m pip install --upgrade pip
"$DEST/.venv/bin/pip" install -r "$DEST/requirements.txt"

cat > "$BIN_DIR/auralyn-click" <<EOF
#!/usr/bin/env bash
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_ENABLE_HIGHDPI_SCALING=1
export PYTHONPATH="$DEST/src"
exec "$DEST/.venv/bin/python" -m auralyn_click "\$@"
EOF
chmod +x "$BIN_DIR/auralyn-click"

cp "$ROOT/auralyn-click-control.py" "$BIN_DIR/auralyn-click-control"
chmod +x "$BIN_DIR/auralyn-click-control"
cp "$ROOT/assets/auralyn-click.png" "$ICON_DIR/auralyn-click.png"

cat > "$APP_DIR/auralyn-click.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Auralyn Click
GenericName=Auto Clicker
Comment=Modern auto clicker with global hotkeys and themes
Exec=$BIN_DIR/auralyn-click
Icon=$DEST/assets/auralyn-click.png
Terminal=false
Categories=Utility;
StartupNotify=true
StartupWMClass=AuralynClick
X-GNOME-WMClass=AuralynClick
Keywords=click;autoclicker;mouse;auralyn;
EOF
chmod +x "$APP_DIR/auralyn-click.desktop"

DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
if [ -z "${DESKTOP_DIR:-}" ]; then [ -d "$HOME/Schreibtisch" ] && DESKTOP_DIR="$HOME/Schreibtisch" || DESKTOP_DIR="$HOME/Desktop"; fi
mkdir -p "$DESKTOP_DIR"
cp "$APP_DIR/auralyn-click.desktop" "$DESKTOP_DIR/Auralyn-Click.desktop"
chmod +x "$DESKTOP_DIR/Auralyn-Click.desktop"
if command -v gio >/dev/null 2>&1; then gio set "$DESKTOP_DIR/Auralyn-Click.desktop" metadata::trusted true 2>/dev/null || true; fi

if command -v gsettings >/dev/null 2>&1 && gsettings list-schemas | grep -qx 'org.gnome.settings-daemon.plugins.media-keys'; then
  TOGGLE_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/auralyn-click-toggle/"
  CAPTURE_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/auralyn-click-capture/"
  STOP_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/auralyn-click-stop/"
  CURRENT="$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings 2>/dev/null || echo '[]')"
  NEW_LIST="$(python3 - "$CURRENT" "$TOGGLE_PATH" "$CAPTURE_PATH" "$STOP_PATH" <<'PY2'
import ast, sys
raw=sys.argv[1].strip(); paths=sys.argv[2:]
if raw.startswith('@as '): raw=raw[4:].strip()
try: arr=ast.literal_eval(raw)
except Exception: arr=[]
if not isinstance(arr,list): arr=[]
for p in paths:
    if p not in arr: arr.append(p)
print(repr(arr))
PY2
)"
  gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$NEW_LIST"
  SCHEMA="org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"
  gsettings set "$SCHEMA:$TOGGLE_PATH" name "'Auralyn Click F6 Toggle'"
  gsettings set "$SCHEMA:$TOGGLE_PATH" command "'$BIN_DIR/auralyn-click-control toggle'"
  gsettings set "$SCHEMA:$TOGGLE_PATH" binding "'F6'"
  gsettings set "$SCHEMA:$CAPTURE_PATH" name "'Auralyn Click F7 Position'"
  gsettings set "$SCHEMA:$CAPTURE_PATH" command "'$BIN_DIR/auralyn-click-control capture'"
  gsettings set "$SCHEMA:$CAPTURE_PATH" binding "'F7'"
  gsettings set "$SCHEMA:$STOP_PATH" name "'Auralyn Click F8 Emergency Stop'"
  gsettings set "$SCHEMA:$STOP_PATH" command "'$BIN_DIR/auralyn-click-control stop'"
  gsettings set "$SCHEMA:$STOP_PATH" binding "'F8'"
fi

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true

printf '\nAuralyn Click installed.\nRun: auralyn-click\nSettings: ~/.config/auralyn-click/settings.json\n\n'
nohup "$BIN_DIR/auralyn-click" >/dev/null 2>&1 &
