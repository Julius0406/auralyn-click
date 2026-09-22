# Changelog

## 2.4.1 — release cleanup and documentation

- refreshed the public README for Windows and Linux
- standardized author and publisher metadata as Julius04-06
- removed the stale 2.2.0 commit message from the publishing helper
- versioned the generated GitHub source ZIP correctly
- added the source ZIP to automatic GitHub Release assets
- cleaned package descriptions so the project is presented as cross-platform
- kept the existing 2.4 setup, installer and first-run features

## 2.4.0 — graphical installers and first-run setup

- added a built-in first-run setup wizard for Windows and Linux
- added language, theme, accent, background, animation FPS and startup-screen choices to setup
- added optional per-user start-at-login support
- added a Windows Inno Setup personalization page
- Windows installer can create desktop and autostart entries without admin rights
- Linux `.deb` now includes an **Auralyn Click Setup** launcher
- Linux first launch opens the setup wizard automatically
- setup can be reopened later from the settings drawer
- existing user settings are preserved during upgrades
- fixed cross-platform restart handling when applying language/setup changes

## 2.3.0

- Added Windows 10/11 support.
- Added cross-platform single-instance and IPC handling.
- Added native global F6/F7/F8 hotkeys on Windows.
- Added Windows PyInstaller and Inno Setup release pipeline.
- Added standalone Linux `.deb` and portable build pipeline.
- Added automatic GitHub Release workflow for version tags.
- Made settings paths platform-aware.
- Cleaned release documentation for the public repository.

## 2.2.0 — Smooth scrolling + multilingual UI

- fixed heavy scroll stutter caused by animated transparent backgrounds
- decorative background animation now pauses briefly while scrolling and resumes automatically
- custom images/GIFs are cached instead of being re-scaled on every paint
- Live Orb animation reduced from ~166 repaint requests/s to a stable 60 Hz
- resize styling is debounced to avoid repeated full stylesheet rebuilds
- procedural background renderer uses fewer expensive paint operations
- added optional **Smooth scrolling mode** in Display & Design
- added automatic Linux system-language detection
- added **24 selectable languages** plus System/Auto mode
- language can be changed from the gear menu and applied with an automatic restart
- added RTL layout support for Arabic
- packaged app icon inside the Python package for more reliable installs

## 2.1.0 — first public GitHub edition

- new application identity and icon
- fullscreen, compact or disabled startup screen
- splash uses selected theme and background
- animated Aurora, Nebula, Grid Waves and Particles backgrounds
- static gradient background
- custom PNG/JPG/WEBP/GIF backgrounds
- animated settings drawer opened with gear button
- selectable background FPS: 30/60/120/160
- animated segmented controls, start glow and window entrance
- direct CPS timing mode
- triple click
- click hold duration
- start delay
- time limit
- burst mode
- random fixed-position radius
- session timer
- GitHub publish helper script
- MIT license and GitHub-ready README
