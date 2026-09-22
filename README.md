# Auralyn Click

<p align="center">
  <img src="assets/auralyn-click.png" width="150" alt="Auralyn Click icon">
</p>

<p align="center">
  <strong>A modern, animated and deeply customizable auto clicker for Linux.</strong><br>
  Built with Python + Qt 6. Designed by Julius.
</p>

> **Project status:** Beta / active development. Linux-first, especially Ubuntu + GNOME.

## ✨ Why Auralyn Click?

Auralyn Click started as a small personal auto clicker and was rewritten as a proper Qt 6 desktop app with a focus on design, smooth motion, Linux integration, safety controls and customization.

It is intentionally **not** an anti-cheat bypass. Some games and services prohibit auto clickers, so check the rules of the software/server where you use it.

## 🎨 UI, themes and backgrounds

Auralyn Click includes a dedicated **gear menu** that slides in with an animation.

### Themes

- Midnight
- AMOLED
- Light

### Accent colors

- Violet
- Cyan
- Emerald
- Sunset
- Rose

### Built-in backgrounds

- **Aurora** — animated moving color fields and light waves
- **Nebula** — moving clouds + pulsing stars
- **Grid Waves** — animated futuristic grid
- **Particles** — floating particles
- **Static Gradient** — low-power static option
- **Custom** — your own PNG, JPG, WEBP or animated GIF

Custom backgrounds are copied to:

```text
~/.config/auralyn-click/
```

so they do not disappear if the original file is moved later.

### Motion quality

Background animation can run at:

- 30 FPS
- 60 FPS
- 120 FPS
- 160 FPS

The actual visible refresh rate is still limited by your monitor and Linux compositor.

### Smooth scrolling performance mode

Auralyn Click 2.2 adds a scroll-aware renderer. While you actively scroll, expensive decorative animation is paused for a fraction of a second so the Qt scroll area gets the frame budget. As soon as scrolling stops, the selected animated background resumes automatically.

Other performance fixes in 2.2:

- the Live Orb now animates at a stable 60 Hz instead of requesting ~166 repaints per second
- custom images and GIF frames are cached at the current window size instead of being scaled during every paint
- resize styling is debounced so a resize does not rebuild the full Qt stylesheet dozens of times
- procedural effects use fewer expensive paint operations

You can disable **Smooth scrolling mode** in the gear menu if you prefer the background to keep animating during scroll input.

## 🌍 Languages

The default language is **System / Auto**. Auralyn Click reads the Linux locale (`LANG`, `LC_MESSAGES` or `LC_ALL`) and chooses a supported language automatically.

You can override it from the gear menu and use **Apply language & restart**. The selected language is saved in `~/.config/auralyn-click/settings.json`.

Auralyn Click currently exposes **24 selectable languages**:

- German (Deutsch)
- English
- French (Français)
- Spanish (Español)
- Italian (Italiano)
- Portuguese (Português)
- Dutch (Nederlands)
- Polish (Polski)
- Czech (Čeština)
- Slovak (Slovenčina)
- Hungarian (Magyar)
- Romanian (Română)
- Swedish (Svenska)
- Norwegian (Norsk)
- Danish (Dansk)
- Finnish (Suomi)
- Turkish (Türkçe)
- Russian (Русский)
- Ukrainian (Українська)
- Greek (Ελληνικά)
- Japanese (日本語)
- Korean (한국어)
- Chinese (中文)
- Arabic (العربية, with RTL layout)

Some technical terms such as CPS/FPS and product/theme names intentionally stay unchanged across languages.

## 🚀 Start screen

The splash/loading screen uses your currently selected theme and background.

It shows:

- large Auralyn Click logo
- large `Auralyn Click` title
- animated background
- progress animation
- `By Julius` centered at the bottom

You can choose:

- **Fullscreen**
- **Compact**
- **Off**

and change the display duration in Settings.

## 🖱️ Auto-clicker features

### Timing

- interval mode down to **1 ms**
- direct **CPS mode** from 1–1000 CPS
- quick presets: 10 CPS, 20 CPS, 100 CPS and 1 ms
- optional random delay/jitter

### Click style

- left click
- right click
- middle click
- single click
- double click
- triple click
- optional press/hold duration per click

### Position

- click at the current cursor position
- fixed X/Y position
- F7 captures the current cursor position
- optional random position radius around a fixed point

### Session controls

- infinite mode
- fixed action count
- configurable start delay
- optional time limit
- burst mode: click N times, pause, continue
- live CPS
- total click counter
- session timer

### Safety

- **F6** — global Start / Stop
- **F7** — capture cursor position
- **F8** — dedicated emergency stop; it only stops and never starts clicking
- single-instance lock: opening Auralyn Click twice brings the existing window forward instead of creating another click engine

## 💾 Settings

Settings are saved automatically and restored on the next launch:

```text
~/.config/auralyn-click/settings.json
```

On the first launch, Auralyn Click can automatically import compatible settings from the old PulseClick configuration at:

```text
~/.config/pulseclick/settings.json
```

The old file is not deleted.

## 🧰 Technology

- **Language:** Python 3.10+
- **GUI:** Qt 6 through PySide6
- **Localization:** built-in JSON-style Python translation tables with Linux locale auto-detection
- **Input automation:** pynput
- **Global Ubuntu/GNOME shortcuts:** GNOME `gsettings` custom shortcuts
- **Local app control:** Unix domain socket
- **Single-instance protection:** Linux `flock`
- **License:** MIT

## 📦 Install on Ubuntu

### Upgrading from the old PulseClick build

If PulseClick is already installed on your PC, use the migration script. It installs Auralyn Click, removes the old PulseClick launchers so F6/F7/F8 do not conflict, and keeps the old program files/settings as a backup:

```bash
chmod +x scripts/upgrade-from-pulseclick.sh
./scripts/upgrade-from-pulseclick.sh
```

### Updating an existing Auralyn Click install

Version 2.2 includes a dedicated updater that keeps your existing settings:

```bash
chmod +x scripts/update.sh
./scripts/update.sh
```

Your config in `~/.config/auralyn-click/` is not reset.

### Fresh install

Extract or clone the repository, then run:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

The installer:

1. installs/checks Ubuntu Python runtime packages,
2. creates an isolated Python virtual environment,
3. installs PySide6 and pynput,
4. installs the Auralyn Click source under `~/.local/share/auralyn-click`,
5. creates `~/.local/bin/auralyn-click`,
6. installs the desktop launcher and icon,
7. configures F6/F7/F8 as GNOME global shortcuts when available,
8. starts the app.

Afterwards you can launch it with:

```bash
auralyn-click
```

or from the Ubuntu app menu / desktop icon.

## 🧪 Run from source

```bash
git clone YOUR_REPOSITORY_URL
cd auralyn-click
chmod +x scripts/run-dev.sh
./scripts/run-dev.sh
```

The development script creates `.venv` automatically on first run.

## 🌐 Wayland note

Ubuntu/Wayland may ask you to allow simulated input. If Linux displays a permission prompt for input control, approve it if you want Auralyn Click to click outside its own window.

The F6/F7/F8 GNOME shortcuts are registered separately, so the emergency stop does not depend on the Auralyn Click window having focus.

If synthetic mouse input is blocked completely by your Wayland setup, an Xorg session may be more compatible.

## ⚙️ Global shortcut troubleshooting

Open:

```text
Settings → Keyboard → Keyboard Shortcuts / Custom Shortcuts
```

You should see entries similar to:

```text
Auralyn Click F6 Toggle
Auralyn Click F7 Position
Auralyn Click F8 Emergency Stop
```

Make sure F6/F7/F8 are not already assigned to conflicting custom shortcuts.

## 📤 Publish this project to GitHub

A helper script is included. It uses the official GitHub CLI (`gh`).

First make sure GitHub CLI is installed and logged in:

```bash
sudo apt install gh
gh auth login
```

Git also needs your commit identity once:

```bash
git config --global user.name "Julius"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

Then publish as a public repository:

```bash
./scripts/publish-github.sh public auralyn-click
```

Or private:

```bash
./scripts/publish-github.sh private auralyn-click
```

The script initializes Git if needed, creates an initial commit, creates the GitHub repository when it does not exist, adds `origin` and pushes `main`.

## 🗜️ Build a source ZIP

```bash
./scripts/build-source-zip.sh
```

## 🧹 Uninstall

```bash
./scripts/uninstall.sh
```

The uninstall script intentionally keeps your settings in `~/.config/auralyn-click/`.

## 📁 Repository structure

```text
AuralynClick/
├── assets/                         # GitHub/readme artwork
├── src/auralyn_click/
│   ├── assets/                     # packaged application icons
│   ├── backgrounds.py              # Aurora/Nebula/Grid/Particles/custom renderer
│   ├── click_engine.py             # click worker and advanced click logic
│   ├── ipc.py                      # single-instance + local global-hotkey bridge
│   ├── main.py                     # Qt application, splash, settings drawer
│   ├── settings.py                 # persistent settings + PulseClick migration
│   ├── widgets.py                  # animated reusable Qt widgets
│   ├── __init__.py
│   └── __main__.py
├── scripts/
│   ├── install.sh
│   ├── upgrade-from-pulseclick.sh
│   ├── run-dev.sh
│   ├── uninstall.sh
│   ├── publish-github.sh
│   └── build-source-zip.sh
├── auralyn-click-control.py        # command bridge used by global shortcuts
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## 🔒 Privacy

The application itself does not contain telemetry, advertising, account tracking or analytics code. Settings and custom backgrounds are stored locally on the computer.

Dependency installation obviously requires internet access when packages are not already cached.

## 🙏 Credits

- **Concept, design direction and project owner:** Julius
- **Development assistance:** OpenAI ChatGPT
- **GUI framework:** Qt / PySide6 by The Qt Company / Qt for Python project
- **Input library:** pynput contributors

## 📄 License

MIT License. See [`LICENSE`](LICENSE).

## ⚠️ Disclaimer

Auralyn Click is a general desktop automation utility. The project does not include anti-cheat bypasses or stealth features. You are responsible for following the rules, terms of service and policies of the apps, games and servers where you use it.
