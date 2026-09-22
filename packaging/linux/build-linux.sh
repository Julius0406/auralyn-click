#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="$(PYTHONPATH="$ROOT/src" python3 -c 'from auralyn_click import __version__; print(__version__)')"
BUILD="$ROOT/build/linux"
RELEASE="$ROOT/release"
rm -rf "$BUILD" "$ROOT/dist/AuralynClick"
mkdir -p "$BUILD" "$RELEASE"
python3 -m pip install -U pip
python3 -m pip install -r "$ROOT/requirements.txt" pyinstaller
python3 -m PyInstaller --noconfirm --clean --windowed \
  --name AuralynClick \
  --icon "$ROOT/assets/auralyn-click.png" \
  --paths "$ROOT/src" \
  --add-data "$ROOT/src/auralyn_click/assets:auralyn_click/assets" \
  --hidden-import pynput.keyboard._xorg \
  --hidden-import pynput.mouse._xorg \
  "$ROOT/packaging/entry.py"

tar -C "$ROOT/dist" -czf "$RELEASE/AuralynClick-$VERSION-linux-x86_64-portable.tar.gz" AuralynClick

PKG="$BUILD/deb"
mkdir -p "$PKG/DEBIAN" "$PKG/opt/auralyn-click" "$PKG/usr/bin" "$PKG/usr/share/applications" "$PKG/usr/share/icons/hicolor/512x512/apps"
cp -r "$ROOT/dist/AuralynClick/." "$PKG/opt/auralyn-click/"
ln -s /opt/auralyn-click/AuralynClick "$PKG/usr/bin/auralyn-click"
cp "$ROOT/assets/auralyn-click.png" "$PKG/usr/share/icons/hicolor/512x512/apps/auralyn-click.png"
cat > "$PKG/DEBIAN/control" <<EOF
Package: auralyn-click
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Julius0406
Description: Modern cross-platform auto clicker for Windows and Linux
EOF
cat > "$PKG/usr/share/applications/auralyn-click.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Auralyn Click
Comment=Modern auto clicker with global hotkeys and themes
Exec=/usr/bin/auralyn-click
Icon=auralyn-click
Terminal=false
Categories=Utility;
StartupWMClass=AuralynClick
EOF
cat > "$PKG/usr/share/applications/auralyn-click-setup.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Auralyn Click Setup
Comment=Open the Auralyn Click setup wizard
Exec=/usr/bin/auralyn-click --setup
Icon=auralyn-click
Terminal=false
Categories=Utility;Settings;
StartupWMClass=AuralynClick
EOF
chmod 755 "$PKG/DEBIAN" "$PKG/opt/auralyn-click" "$PKG/usr/bin"
dpkg-deb --build --root-owner-group "$PKG" "$RELEASE/AuralynClick-$VERSION-linux-amd64.deb"
echo "Built Linux release assets in $RELEASE"
