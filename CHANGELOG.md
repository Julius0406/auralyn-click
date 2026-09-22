# Changelog

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

## 2.1.0 — Auralyn Click rename / GitHub edition

- renamed PulseClick to Auralyn Click
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
- automatic migration from PulseClick settings
- GitHub publish helper script
- MIT license and GitHub-ready README
