from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from .i18n import SUPPORTED_CODES

APP_SLUG = "auralyn-click"

def _config_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "AuralynClick"
    return Path.home() / ".config" / APP_SLUG

CONFIG_DIR = _config_dir()
SETTINGS_PATH = CONFIG_DIR / "settings.json"

DEFAULTS: dict[str, Any] = {
    # Click engine
    "timing_mode": "interval",  # interval | cps
    "hours": 0,
    "minutes": 0,
    "seconds": 0,
    "millis": 100,
    "cps": 10,
    "button": "left",  # left | right | middle
    "click_type": "single",  # single | double | triple
    "repeat_mode": "infinite",  # infinite | count
    "repeat_count": 100,
    "position_mode": "current",  # current | fixed
    "pos_x": 0,
    "pos_y": 0,
    "random_delay": False,
    "random_delay_ms": 5,
    "random_position": False,
    "random_position_radius": 3,
    "press_duration_ms": 0,
    "start_delay_ms": 0,
    "burst_enabled": False,
    "burst_count": 10,
    "burst_pause_ms": 250,
    "time_limit_enabled": False,
    "time_limit_seconds": 60,
    # Appearance
    "theme": "Midnight",
    "accent": "Violet",
    "background": "Aurora",
    "custom_background": "",
    "background_fps": 60,
    "animations": True,
    "ui_scale": 100,
    "language": "system",
    "smooth_scrolling": True,
    # Splash / startup
    "startup_screen": "fullscreen",  # fullscreen | compact | off
    "startup_duration_ms": 1800,
    "monitor_index": 0,  # 0-based Qt screen index
    # First-run setup / integration
    "setup_completed": False,
    "autostart": False,
}

VALID = {
    "timing_mode": {"interval", "cps"},
    "button": {"left", "right", "middle"},
    "click_type": {"single", "double", "triple"},
    "repeat_mode": {"infinite", "count"},
    "position_mode": {"current", "fixed"},
    "theme": {"Midnight", "AMOLED", "Light"},
    "accent": {"Violet", "Cyan", "Emerald", "Sunset", "Rose"},
    "background": {"Aurora", "Nebula", "Grid Waves", "Particles", "Static Gradient", "Custom"},
    "startup_screen": {"fullscreen", "compact", "off"},
    "background_fps": {30, 60, 120, 160},
    "language": SUPPORTED_CODES,
}


def _clamp_int(value: Any, low: int, high: int, fallback: int) -> int:
    try:
        return max(low, min(high, int(value)))
    except Exception:
        return fallback


def load_settings() -> dict[str, Any]:
    data = dict(DEFAULTS)
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if SETTINGS_PATH.exists():
            with SETTINGS_PATH.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data.update({k: v for k, v in loaded.items() if k in DEFAULTS})
    except Exception:
        pass

    for key, allowed in VALID.items():
        if data.get(key) not in allowed:
            data[key] = DEFAULTS[key]

    int_rules = {
        "hours": (0, 99),
        "minutes": (0, 59),
        "seconds": (0, 59),
        "millis": (0, 999),
        "cps": (1, 1000),
        "repeat_count": (1, 999_999_999),
        "pos_x": (-99999, 99999),
        "pos_y": (-99999, 99999),
        "random_delay_ms": (0, 10000),
        "random_position_radius": (0, 1000),
        "press_duration_ms": (0, 10000),
        "start_delay_ms": (0, 60000),
        "burst_count": (1, 100000),
        "burst_pause_ms": (0, 60000),
        "time_limit_seconds": (1, 86400),
        "ui_scale": (80, 140),
        "startup_duration_ms": (400, 5000),
        "monitor_index": (0, 31),
    }
    for key, (lo, hi) in int_rules.items():
        data[key] = _clamp_int(data.get(key), lo, hi, DEFAULTS[key])

    for key in (
        "random_delay",
        "random_position",
        "burst_enabled",
        "time_limit_enabled",
        "animations",
        "smooth_scrolling",
        "setup_completed",
        "autostart",
    ):
        data[key] = bool(data.get(key))

    return data


def save_settings(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SETTINGS_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, SETTINGS_PATH)


def import_custom_background(source: str) -> str:
    """Copy a custom image/GIF into the app config so it keeps working later."""
    src = Path(source)
    if not src.is_file():
        return ""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    suffix = src.suffix.lower() or ".png"
    dest = CONFIG_DIR / f"custom-background{suffix}"
    try:
        if dest.exists():
            dest.unlink()
        shutil.copy2(src, dest)
        return str(dest)
    except Exception:
        return str(src)
