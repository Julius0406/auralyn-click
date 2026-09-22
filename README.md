# Auralyn Click

<p align="center">
  <img src="assets/auralyn-click.png" width="150" alt="Auralyn Click icon">
</p>

<p align="center">
  <strong>A modern and customizable auto clicker for Linux.</strong><br>
  Built with Python and Qt 6. Designed by Julius.
</p>

Auralyn Click is a Linux-first auto clicker with a focus on a clean interface, useful controls, smooth animations and customization. It is currently in active development and is mainly tested on Ubuntu with GNOME.

It is a general desktop automation tool. It does not contain anti-cheat bypasses or stealth features. Some games, servers and services do not allow auto clickers, so check their rules before using it.

## Features

### Clicking

- Click interval down to 1 ms
- CPS mode from 1 to 1000 CPS
- Left, right and middle mouse button
- Single, double and triple click
- Optional click hold duration
- Current cursor position or fixed X/Y position
- Capture the current cursor position with F7
- Optional random position radius
- Optional random delay
- Infinite clicking or a fixed action count
- Start delay
- Optional time limit
- Burst mode with configurable click count and pause
- Live CPS counter
- Total click counter
- Session timer

### Global hotkeys

- **F6** — Start / Stop
- **F7** — Capture cursor position
- **F8** — Emergency stop

F8 is intentionally stop-only, so pressing it can never start the clicker by accident.

Auralyn Click also uses a single-instance lock. Opening the app a second time brings the existing window forward instead of starting another click engine.

## Interface and customization

The interface is built with Qt 6 and includes a separate settings panel for appearance and display options.

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

### Backgrounds

Built-in backgrounds include:

- **Aurora** — animated moving color fields
- **Nebula** — moving clouds and stars
- **Grid Waves** — animated grid effect
- **Particles** — floating particles
- **Static Gradient** — low-power static background
- **Custom** — your own PNG, JPG, WEBP or animated GIF

Custom backgrounds are copied to:

```text
~/.config/auralyn-click/
```

That way they keep working even if the original image is moved later.

### Animation quality

Background animation can be set to:

- 30 FPS
- 60 FPS
- 120 FPS
- 160 FPS

The visible frame rate still depends on the monitor, desktop compositor and system load.

## Performance

Version 2.2 includes several changes aimed at keeping scrolling and resizing smooth.

While you actively scroll, expensive decorative background animation is temporarily reduced so the Qt scroll area gets more rendering time. The selected background resumes automatically when scrolling stops.

Other optimizations include:

- Live status animation runs at a stable 60 Hz instead of requesting unnecessary high-frequency repaints
- custom images and GIF frames are cached at the current window size
- stylesheet updates during resizing are debounced
- procedural backgrounds use fewer expensive paint operations

Smooth scrolling mode can be disabled in the display settings if you prefer backgrounds to keep animating while scrolling.

## Languages

The default language is **System / Auto**. Auralyn Click reads the Linux locale from `LANG`, `LC_MESSAGES` or `LC_ALL` and chooses a supported language automatically.

You can change the language from the settings panel at any time. The selected language is stored in:

```text
~/.config/auralyn-click/settings.json
```

Currently available languages:

- German — Deutsch
- English
- French — Français
- Spanish — Español
- Italian — Italiano
- Portuguese — Português
- Dutch — Nederlands
- Polish — Polski
- Czech — Čeština
- Slovak — Slovenčina
- Hungarian — Magyar
- Romanian — Română
- Swedish — Svenska
- Norwegian — Norsk
- Danish — Dansk
- Finnish — Suomi
- Turkish — Türkçe
- Russian — Русский
- Ukrainian — Українська
- Greek — Ελληνικά
- Japanese — 日本語
- Korean — 한국어
- Chinese — 中文
- Arabic — العربية

Arabic uses right-to-left layout where supported. Technical terms such as CPS and FPS, as well as theme names, may stay unchanged across languages.

## Start screen

The optional start screen uses the selected theme and background.

It can show:

- the Auralyn Click logo
- the Auralyn Click title
- the selected background
- a loading animation
- `By Julius` at the bottom

Available modes:

- Fullscreen
- Compact
- Off

The display duration can also be changed in settings.

## Settings

Settings are saved automatically and restored the next time the app starts.

```text
~/.config/auralyn-click/settings.json
```

This includes click timing, button mode, position settings, design choices, language and display options.

## Requirements

- Linux
- Python 3.10 or newer
- Qt 6 through PySide6
- `pynput`

Auralyn Click is mainly developed and tested on Ubuntu with GNOME. Other Linux desktops may work, but global shortcut behavior can differ.

## Installation on Ubuntu

Clone or extract the repository and run:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

The installer will:

1. check the required Ubuntu/Python packages
2. create an isolated Python virtual environment
3. install PySide6 and pynput
4. install Auralyn Click under `~/.local/share/auralyn-click`
5. create the `auralyn-click` terminal command
6. install the desktop launcher and icon
7. configure F6, F7 and F8 as GNOME global shortcuts when supported
8. start the application

After installation, start it from the Ubuntu app menu or run:

```bash
auralyn-click
```

## Updating

To update an existing Auralyn Click installation while keeping your settings:

```bash
chmod +x scripts/update.sh
./scripts/update.sh
```

Your files in `~/.config/auralyn-click/` are kept.

## Run from source

```bash
git clone YOUR_REPOSITORY_URL
cd auralyn-click
chmod +x scripts/run-dev.sh
./scripts/run-dev.sh
```

The development script creates `.venv` automatically on first run.

## Wayland

On Ubuntu with Wayland, the desktop may ask for permission before an application can simulate mouse input. If you want Auralyn Click to click outside its own window, that permission needs to be allowed.

The F6, F7 and F8 GNOME shortcuts are registered separately, so the emergency stop does not depend on the application window being focused.

If simulated mouse input is blocked completely by your Wayland setup, an Xorg session may be more compatible.

## Global shortcut troubleshooting

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

If a shortcut does not work, make sure the same function key is not already assigned to another custom shortcut.

## Publishing to GitHub

A helper script is included and uses the official GitHub CLI.

Install and sign in to `gh` if needed:

```bash
sudo apt install gh
gh auth login
```

Git also needs a commit identity:

```bash
git config --global user.name "Julius"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

Publish as a public repository:

```bash
./scripts/publish-github.sh public auralyn-click
```

Or as a private repository:

```bash
./scripts/publish-github.sh private auralyn-click
```

The script initializes Git if needed, creates the first commit, creates the GitHub repository if necessary, adds `origin` and pushes the `main` branch.

## Build a source ZIP

```bash
./scripts/build-source-zip.sh
```

## Uninstall

```bash
./scripts/uninstall.sh
```

The uninstall script keeps your settings in `~/.config/auralyn-click/`.

## Project structure

```text
AuralynClick/
├── assets/                         # README and repository artwork
├── src/auralyn_click/
│   ├── assets/                     # application icons and packaged assets
│   ├── backgrounds.py              # animated and custom background renderer
│   ├── click_engine.py             # click worker and click logic
│   ├── ipc.py                      # single-instance and local control bridge
│   ├── main.py                     # Qt application and settings UI
│   ├── settings.py                 # persistent application settings
│   ├── widgets.py                  # reusable Qt widgets and animations
│   ├── __init__.py
│   └── __main__.py
├── scripts/
│   ├── install.sh
│   ├── update.sh
│   ├── run-dev.sh
│   ├── uninstall.sh
│   ├── publish-github.sh
│   └── build-source-zip.sh
├── auralyn-click-control.py        # bridge used by global shortcuts
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## Privacy

Auralyn Click does not include telemetry, advertising, account tracking or analytics code. Settings and custom backgrounds are stored locally on your computer.

An internet connection is only needed when dependencies need to be downloaded or when you use GitHub-related scripts.

## Credits

- Concept, design direction and project owner: **Julius**
- Development assistance: **OpenAI ChatGPT**
- GUI framework: **Qt / PySide6**
- Input library: **pynput**

## License

Auralyn Click is released under the MIT License. See [`LICENSE`](LICENSE).

## Disclaimer

Auralyn Click is a general desktop automation utility. You are responsible for following the rules, terms of service and policies of the applications, games and servers where you use it.
