#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OLD="$HOME/.local/share/pulseclick"
BIN="$HOME/.local/bin"
APP="$HOME/.local/share/applications"

if [ -x "$BIN/pulseclick-control" ]; then
  "$BIN/pulseclick-control" stop 2>/dev/null || true
fi
pkill -f "$OLD/app.py" 2>/dev/null || true

# Install the renamed application first. Its first launch imports compatible settings.
"$ROOT/scripts/install.sh"

# Remove only old launchers/commands to prevent accidentally running both programs.
# The old program files and ~/.config/pulseclick are intentionally preserved as a backup.
rm -f "$BIN/pulseclick" "$BIN/pulseclick-control"
rm -f "$APP/pulseclick.desktop"
rm -f "$HOME/Desktop/PulseClick.desktop" "$HOME/Schreibtisch/PulseClick.desktop"

echo
echo "✅ PulseClick launchers removed; old files/settings were kept as backup."
echo "   New command: auralyn-click"
