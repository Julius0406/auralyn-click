# Auralyn Click

Auralyn Click is a desktop auto clicker for **Windows and Linux**. It is built around fast global controls, flexible click settings, a modern Qt interface and enough visual customization to make it feel like an actual desktop app instead of a small utility window.

The normal release installers are intended for people who just want to install the app and use it. Python and build tools are only needed when working with the source code.

## Downloads

For normal use, download the installer for your operating system from the latest GitHub Release.

### Windows 10 / 11

Use:

```text
AuralynClick-2.4.1-Windows-x64-Setup.exe
```

The Windows setup uses a normal graphical installer. It can create Start Menu and desktop shortcuts, configure startup behavior and choose initial appearance settings before the app is launched for the first time.

A portable ZIP is also built for people who prefer not to install the program.

### Ubuntu / Debian-based Linux

Use:

```text
AuralynClick-2.4.1-linux-amd64.deb
```

Open the `.deb` with your normal software installer and press **Install**. The first launch opens Auralyn Click's setup wizard, where language and display options can be selected without using a terminal.

A portable Linux archive is built alongside the package.

## Main features

### Clicking

- interval mode down to 1 ms
- CPS mode up to 1000 CPS
- left, right and middle mouse button
- single, double and triple click
- unlimited clicking or a fixed number of actions
- start delay and optional session time limit
- burst mode with a configurable pause
- optional mouse-button hold duration
- current cursor position or a fixed position
- random delay and random position radius
- live CPS, click counter and session information

### Global controls

| Key | Action |
| --- | --- |
| `F6` | Start / stop |
| `F7` | Capture current cursor position |
| `F8` | Emergency stop; this key only stops |

Auralyn Click also prevents multiple copies of the app from running at the same time.

### Interface

- Midnight, AMOLED and Light themes
- multiple accent colors
- animated Aurora, Nebula, Grid Waves and Particles backgrounds
- static gradient background
- custom PNG, JPG, WEBP and animated GIF backgrounds
- selectable background frame rate
- responsive layout and high-DPI support
- optional fullscreen or compact startup screen
- animations can be reduced or disabled
- display settings are available from the gear menu

### Languages

The default is **System / Auto**, which follows the operating-system language where a translation is available.

Auralyn Click currently includes 24 selectable interface languages, including German, English, French, Spanish, Italian, Portuguese, Dutch, Polish, Czech, Slovak, Hungarian, Romanian, Swedish, Norwegian, Danish, Finnish, Turkish, Russian, Ukrainian, Greek, Japanese, Korean, Chinese and Arabic.

Arabic uses right-to-left layout support.

## First launch

The first-run setup wizard is available on both Windows and Linux. It can configure:

- language
- theme and accent color
- animated background
- background FPS
- animations
- startup-screen style
- start-at-login behavior

These choices are not permanent. The setup wizard can be opened again from the app later.

## Settings

Settings are saved automatically.

**Linux**

```text
~/.config/auralyn-click/settings.json
```

**Windows**

```text
%APPDATA%\AuralynClick\settings.json
```

## Building from source

This part is for contributors or anyone who wants to modify Auralyn Click.

### Requirements

- Python 3.10+
- Qt 6 through PySide6
- pynput
- PyInstaller for release builds
- Inno Setup 6 for the Windows installer

Install Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

Run the project from source on Linux with:

```bash
./scripts/run-dev.sh
```

On Windows, the development helper is:

```powershell
.\scripts\install-windows-dev.ps1
```

## Building installers

### Windows

The Windows release builder uses PyInstaller and Inno Setup 6:

```powershell
.\packaging\windows\build-windows.ps1
```

It produces the Windows setup executable and portable package in `release/`.

### Linux

```bash
chmod +x packaging/linux/build-linux.sh
./packaging/linux/build-linux.sh
```

This produces the Debian package and portable Linux archive in `release/`.

## GitHub Releases

The repository includes `.github/workflows/release.yml`. Pushing a version tag starts native Windows and Ubuntu runners. They build the release files and attach them to a GitHub Release automatically.

For version 2.4.1:

```bash
./scripts/create-release.sh 2.4.1
```

The release workflow creates assets such as:

```text
AuralynClick-2.4.1-Windows-x64-Setup.exe
AuralynClick-2.4.1-Windows-x64-Portable.zip
AuralynClick-2.4.1-linux-amd64.deb
AuralynClick-2.4.1-linux-x86_64-portable.tar.gz
AuralynClick-2.4.1-GitHub-Source.zip
```

GitHub also provides its own automatic source-code ZIP and tarball for every tagged release.

## Project structure

```text
src/auralyn_click/       main application source
assets/                  app icons
packaging/windows/       Windows release and installer files
packaging/linux/         Linux package builder
scripts/                 development, publishing and release helpers
.github/workflows/       GitHub Actions release workflow
```

## Technology

Auralyn Click is mainly written in **Python** and uses **Qt 6 / PySide6** for the interface. Global mouse and keyboard integration uses **pynput**. Release packages are built with **PyInstaller**, **Inno Setup** on Windows and the Debian package format on Linux.

## Credits

Created and maintained by **Julius04-06**.

Auralyn Click uses PySide6 / Qt and pynput. Those projects remain under their respective licenses.

## License

Auralyn Click is released under the [MIT License](LICENSE).
