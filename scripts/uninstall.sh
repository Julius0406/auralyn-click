#!/usr/bin/env bash
set -euo pipefail
BIN="$HOME/.local/bin"
APP="$HOME/.local/share/applications"
DEST="$HOME/.local/share/auralyn-click"
"$BIN/auralyn-click-control" stop 2>/dev/null || true
pkill -f "$DEST/src/auralyn_click" 2>/dev/null || true
rm -rf "$DEST"
rm -f "$BIN/auralyn-click" "$BIN/auralyn-click-control" "$APP/auralyn-click.desktop"
rm -f "$HOME/Desktop/Auralyn-Click.desktop" "$HOME/Schreibtisch/Auralyn-Click.desktop"
echo "Auralyn Click removed. Settings were kept at ~/.config/auralyn-click/"
