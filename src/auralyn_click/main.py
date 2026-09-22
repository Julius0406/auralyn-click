from __future__ import annotations

import os
import sys
import time
import subprocess
import shlex
import ast
import shutil
from pathlib import Path

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRect,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QWizard,
    QWizardPage,
    QFormLayout,
)
from pynput import keyboard, mouse

from . import __version__
from .backgrounds import AnimatedBackground
from .click_engine import ClickConfig, ClickWorker
from .ipc import IPCBridge, IPCServer, acquire_single_instance, release_single_instance, send_command
from .i18n import language_options, resolve_language, tr
from .settings import import_custom_background, load_settings, save_settings
from .widgets import Card, LiveOrb, SegmentControl

APP_NAME = "Auralyn Click"
APP_SLUG = "auralyn-click"
ASSET_DIR = Path(__file__).resolve().parent / "assets"
ICON_PATH = ASSET_DIR / "auralyn-click.png"

ACCENTS = {
    "Violet": "#7C5CFF",
    "Cyan": "#31C7F2",
    "Emerald": "#35D39A",
    "Sunset": "#FF7A59",
    "Rose": "#FF4D8D",
}

THEMES = {
    "Midnight": {
        "bg": "#090B11",
        "panel": "#121620",
        "panel2": "#181D29",
        "panel3": "#222938",
        "text": "#F6F7FB",
        "muted": "#98A2B5",
        "border": "#2A3244",
        "danger": "#FF5364",
        "success": "#38D39F",
    },
    "AMOLED": {
        "bg": "#000000",
        "panel": "#090A0D",
        "panel2": "#111319",
        "panel3": "#191C24",
        "text": "#FFFFFF",
        "muted": "#969EAD",
        "border": "#252A34",
        "danger": "#FF4E62",
        "success": "#35D39A",
    },
    "Light": {
        "bg": "#EDF1F8",
        "panel": "#FFFFFF",
        "panel2": "#F6F8FC",
        "panel3": "#E8EDF5",
        "text": "#151923",
        "muted": "#667085",
        "border": "#D4DBE8",
        "danger": "#CF3448",
        "success": "#118864",
    },
}

BACKGROUND_NAMES = ["Aurora", "Nebula", "Grid Waves", "Particles", "Static Gradient", "Custom"]


def rgba(hex_color: str, alpha: int) -> str:
    c = QColor(hex_color)
    return f"rgba({c.red()},{c.green()},{c.blue()},{alpha})"


def ensure_linux_global_hotkeys() -> None:
    """Register GNOME F6/F7/F8 shortcuts for packaged Linux installs.

    The source installer also configures these shortcuts, but standalone
    release packages cannot safely write a user's dconf database from a
    root package post-install script. Doing it here runs in the user's
    graphical session and also repairs missing shortcuts automatically.
    """
    if not sys.platform.startswith("linux"):
        return
    gsettings = shutil.which("gsettings")
    if not gsettings:
        return
    try:
        schemas = subprocess.check_output([gsettings, "list-schemas"], text=True)
        if "org.gnome.settings-daemon.plugins.media-keys" not in schemas.splitlines():
            return

        launcher = shutil.which(APP_SLUG)
        if not launcher and getattr(sys, "frozen", False):
            launcher = sys.executable
        if not launcher:
            return

        base_schema = "org.gnome.settings-daemon.plugins.media-keys"
        custom_schema = "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"
        paths = {
            "toggle": "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/auralyn-click-toggle/",
            "capture": "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/auralyn-click-capture/",
            "stop": "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/auralyn-click-stop/",
        }
        raw = subprocess.check_output(
            [gsettings, "get", base_schema, "custom-keybindings"], text=True
        ).strip()
        if raw.startswith("@as "):
            raw = raw[4:].strip()
        try:
            current = ast.literal_eval(raw)
        except Exception:
            current = []
        if not isinstance(current, list):
            current = []
        changed = False
        for path in paths.values():
            if path not in current:
                current.append(path)
                changed = True
        if changed:
            subprocess.run(
                [gsettings, "set", base_schema, "custom-keybindings", repr(current)],
                check=False,
            )

        entries = [
            (paths["toggle"], "Auralyn Click F6 Toggle", f"{launcher} --toggle", "F6"),
            (paths["capture"], "Auralyn Click F7 Position", f"{launcher} --capture", "F7"),
            (paths["stop"], "Auralyn Click F8 Emergency Stop", f"{launcher} --stop", "F8"),
        ]
        for path, name, command, binding in entries:
            schema = f"{custom_schema}:{path}"
            subprocess.run([gsettings, "set", schema, "name", repr(name)], check=False)
            subprocess.run([gsettings, "set", schema, "command", repr(command)], check=False)
            subprocess.run([gsettings, "set", schema, "binding", repr(binding)], check=False)
    except Exception as exc:
        print("Auralyn Click hotkey setup skipped:", exc)


def _launch_command() -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable]
    return [sys.executable, "-m", "auralyn_click"]


def set_autostart(enabled: bool) -> None:
    """Enable or disable per-user autostart without requiring admin rights."""
    try:
        if sys.platform.startswith("win"):
            import winreg
            key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                if enabled:
                    command = subprocess.list2cmdline(_launch_command() + ["--show"])
                    winreg.SetValueEx(key, "AuralynClick", 0, winreg.REG_SZ, command)
                else:
                    try:
                        winreg.DeleteValue(key, "AuralynClick")
                    except FileNotFoundError:
                        pass
            return

        if sys.platform.startswith("linux"):
            autostart_dir = Path.home() / ".config" / "autostart"
            desktop = autostart_dir / "auralyn-click.desktop"
            if not enabled:
                try:
                    desktop.unlink()
                except FileNotFoundError:
                    pass
                return
            autostart_dir.mkdir(parents=True, exist_ok=True)
            executable = shutil.which(APP_SLUG)
            if not executable and getattr(sys, "frozen", False):
                executable = sys.executable
            if not executable:
                executable = f'{sys.executable} -m auralyn_click'
            desktop.write_text(
                "[Desktop Entry]\\n"
                "Type=Application\\n"
                "Name=Auralyn Click\\n"
                f"Exec={executable} --show\\n"
                "Terminal=false\\n"
                "X-GNOME-Autostart-enabled=true\\n",
                encoding="utf-8",
            )
    except Exception as exc:
        print("Auralyn Click autostart setup skipped:", exc)


class SetupWizard(QWizard):
    """First-run setup used by packaged Windows and Linux releases."""

    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Auralyn Click Setup")
        self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.setWizardStyle(QWizard.ModernStyle)
        self.resize(760, 560)
        self.setMinimumSize(680, 500)

        self._build_welcome()
        self._build_language()
        self._build_appearance()
        self._build_startup()
        self._build_finish()

        self.setButtonText(QWizard.BackButton, "Back")
        self.setButtonText(QWizard.NextButton, "Next")
        self.setButtonText(QWizard.FinishButton, "Finish")
        self.setButtonText(QWizard.CancelButton, "Cancel")
        self._apply_style()

    def _page(self, title: str, subtitle: str = "") -> tuple[QWizardPage, QVBoxLayout]:
        page = QWizardPage()
        page.setTitle(title)
        page.setSubTitle(subtitle)
        lay = QVBoxLayout(page)
        lay.setSpacing(14)
        return page, lay

    def _build_welcome(self) -> None:
        page, lay = self._page(
            "Welcome to Auralyn Click",
            "A short setup so the app looks and behaves the way you want from the first launch.",
        )
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setPixmap(QIcon(str(ICON_PATH)).pixmap(150, 150))
        lay.addStretch(1)
        lay.addWidget(logo)
        text = QLabel("No terminal is needed. These settings can be changed again later from the gear menu.")
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignCenter)
        lay.addWidget(text)
        lay.addStretch(1)
        self.addPage(page)

    def _build_language(self) -> None:
        page, lay = self._page("Language", "System / Auto follows the language configured in Windows or Linux.")
        form = QFormLayout()
        self.setup_language = QComboBox()
        self.setup_language.addItem("System / Auto", "system")
        for code, name in language_options():
            if code != "system":
                self.setup_language.addItem(name, code)
        idx = self.setup_language.findData(self.settings.get("language", "system"))
        self.setup_language.setCurrentIndex(max(0, idx))
        form.addRow("Language", self.setup_language)
        lay.addLayout(form)
        lay.addStretch(1)
        self.addPage(page)

    def _build_appearance(self) -> None:
        page, lay = self._page("Appearance", "Pick a starting look. Everything stays changeable later.")
        form = QFormLayout()
        self.setup_theme = QComboBox(); self.setup_theme.addItems(THEMES.keys()); self.setup_theme.setCurrentText(self.settings.get("theme", "Midnight"))
        self.setup_accent = QComboBox(); self.setup_accent.addItems(ACCENTS.keys()); self.setup_accent.setCurrentText(self.settings.get("accent", "Violet"))
        self.setup_background = QComboBox(); self.setup_background.addItems([x for x in BACKGROUND_NAMES if x != "Custom"]); self.setup_background.setCurrentText(self.settings.get("background", "Aurora") if self.settings.get("background") != "Custom" else "Aurora")
        self.setup_fps = QComboBox(); self.setup_fps.addItems(["30", "60", "120", "160"]); self.setup_fps.setCurrentText(str(self.settings.get("background_fps", 60)))
        self.setup_animations = QCheckBox("Enable animations")
        self.setup_animations.setChecked(bool(self.settings.get("animations", True)))
        form.addRow("Theme", self.setup_theme)
        form.addRow("Accent", self.setup_accent)
        form.addRow("Background", self.setup_background)
        form.addRow("Background FPS", self.setup_fps)
        form.addRow("", self.setup_animations)
        lay.addLayout(form)
        lay.addStretch(1)
        self.addPage(page)

    def _build_startup(self) -> None:
        page, lay = self._page("Startup", "Choose how Auralyn Click starts on this computer.")
        form = QFormLayout()
        self.setup_splash = QComboBox()
        self.setup_splash.addItem("Fullscreen", "fullscreen")
        self.setup_splash.addItem("Compact", "compact")
        self.setup_splash.addItem("Off", "off")
        idx = self.setup_splash.findData(self.settings.get("startup_screen", "fullscreen"))
        self.setup_splash.setCurrentIndex(max(0, idx))
        self.setup_autostart = QCheckBox("Start Auralyn Click when I sign in")
        self.setup_autostart.setChecked(bool(self.settings.get("autostart", False)))
        form.addRow("Start screen", self.setup_splash)
        form.addRow("", self.setup_autostart)
        lay.addLayout(form)
        hotkeys = QLabel("Global hotkeys: F6 Start/Stop   •   F7 Capture position   •   F8 Emergency Stop")
        hotkeys.setWordWrap(True)
        lay.addWidget(hotkeys)
        lay.addStretch(1)
        self.addPage(page)

    def _build_finish(self) -> None:
        page, lay = self._page("Ready", "Auralyn Click is ready to use.")
        label = QLabel(
            "Click Finish to save these choices. You can reopen this setup later from Settings → Setup Wizard."
        )
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        lay.addStretch(1)
        lay.addWidget(label)
        lay.addStretch(1)
        self.addPage(page)

    def _apply_style(self) -> None:
        pal = THEMES.get(self.settings.get("theme", "Midnight"), THEMES["Midnight"])
        accent = ACCENTS.get(self.settings.get("accent", "Violet"), ACCENTS["Violet"])
        self.setStyleSheet(f"""
            QWizard {{ background: {pal['bg']}; color: {pal['text']}; }}
            QWizardPage {{ background: {pal['bg']}; color: {pal['text']}; }}
            QLabel {{ color: {pal['text']}; font-size: 14px; }}
            QComboBox {{ min-height: 38px; background: {pal['panel2']}; color: {pal['text']}; border: 1px solid {pal['border']}; border-radius: 9px; padding: 0 10px; }}
            QCheckBox {{ color: {pal['text']}; spacing: 8px; }}
            QPushButton {{ min-height: 38px; border-radius: 9px; padding: 0 16px; background: {pal['panel2']}; color: {pal['text']}; border: 1px solid {pal['border']}; font-weight: 700; }}
            QPushButton:hover {{ border-color: {accent}; }}
        """)

    def accept(self) -> None:
        self.settings.update({
            "language": self.setup_language.currentData(),
            "theme": self.setup_theme.currentText(),
            "accent": self.setup_accent.currentText(),
            "background": self.setup_background.currentText(),
            "background_fps": int(self.setup_fps.currentText()),
            "animations": self.setup_animations.isChecked(),
            "startup_screen": self.setup_splash.currentData(),
            "autostart": self.setup_autostart.isChecked(),
            "setup_completed": True,
        })
        save_settings(self.settings)
        set_autostart(self.setup_autostart.isChecked())
        super().accept()


class SplashScreen(AnimatedBackground):
    finished = Signal()

    def __init__(self, settings: dict):
        super().__init__()
        self.settings = settings
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        pal = THEMES.get(settings["theme"], THEMES["Midnight"])
        accent = ACCENTS.get(settings["accent"], ACCENTS["Violet"])
        self.configure(
            mode=settings["background"],
            theme_bg=pal["bg"],
            accent=accent,
            animations=settings["animations"],
            fps=settings["background_fps"],
            custom_path=settings.get("custom_background", ""),
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 28)
        layout.addStretch(1)

        center = QVBoxLayout()
        center.setSpacing(16)

        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setPixmap(QIcon(str(ICON_PATH)).pixmap(170, 170))
        center.addWidget(self.logo)

        self.title = QLabel(APP_NAME)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f"font-size: 58px; font-weight: 900; color: {pal['text']};")
        center.addWidget(self.title)

        self.sub = QLabel(tr(settings.get("language", "system"), "startup_tagline"))
        self.sub.setAlignment(Qt.AlignCenter)
        self.sub.setStyleSheet(f"font-size: 17px; color: {pal['muted']}; font-weight: 600;")
        center.addWidget(self.sub)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(7)
        self.progress.setMaximumWidth(520)
        self.progress.setStyleSheet(
            f"QProgressBar{{background:rgba(255,255,255,35);border:none;border-radius:3px;}}"
            f"QProgressBar::chunk{{background:{accent};border-radius:3px;}}"
        )
        progress_row = QHBoxLayout()
        progress_row.addStretch(1)
        progress_row.addWidget(self.progress, 1)
        progress_row.addStretch(1)
        center.addLayout(progress_row)

        layout.addLayout(center)
        layout.addStretch(1)

        by = QLabel("By Julius")
        by.setAlignment(Qt.AlignCenter)
        by.setStyleSheet(f"font-size: 13px; color: {pal['muted']}; font-weight: 700;")
        layout.addWidget(by)

        self._start = time.perf_counter()
        self._duration = max(400, int(settings["startup_duration_ms"]))
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._tick_splash)

        if settings["startup_screen"] == "fullscreen":
            self.showFullScreen()
        else:
            self.resize(900, 520)
            screen = QGuiApplication.primaryScreen().availableGeometry()
            self.move(screen.center() - self.rect().center())
            self.show()

        if settings.get("animations", True):
            effect = QGraphicsOpacityEffect(self)
            self.setGraphicsEffect(effect)
            self._fade = QPropertyAnimation(effect, b"opacity", self)
            self._fade.setDuration(360)
            self._fade.setStartValue(0.0)
            self._fade.setEndValue(1.0)
            self._fade.setEasingCurve(QEasingCurve.OutCubic)
            self._fade.start()

        self._timer.start()

    def _tick_splash(self) -> None:
        elapsed = (time.perf_counter() - self._start) * 1000.0
        progress = min(100, round(elapsed / self._duration * 100))
        self.progress.setValue(progress)
        if elapsed >= self._duration:
            self._timer.stop()
            self.finished.emit()
            self.close()


class SettingsDrawer(QFrame):
    appearance_changed = Signal()
    choose_background = Signal()
    close_requested = Signal()

    def __init__(self, owner: "AuralynWindow"):
        super().__init__(owner.root)
        self.owner = owner
        self.setObjectName("settingsDrawer")
        self.setMinimumWidth(370)
        self.setMaximumWidth(470)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 16, 18, 18)
        outer.setSpacing(12)

        head = QHBoxLayout()
        title = QLabel(owner.t("display_design"))
        title.setObjectName("drawerTitle")
        head.addWidget(title)
        head.addStretch(1)
        close = QPushButton("✕")
        close.setObjectName("iconButton")
        close.setFixedWidth(46)
        close.clicked.connect(self.close_requested)
        head.addWidget(close)
        outer.addLayout(head)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content = QWidget()
        content.setObjectName("transparent")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        language_card = Card(owner.t("language"), owner.t("language_note"))
        lang_row = QHBoxLayout()
        self.language = QComboBox()
        self.language.addItem(owner.t("system_default"), "system")
        for code, native_name in language_options():
            if code != "system":
                self.language.addItem(native_name, code)
        current_language = owner.settings.get("language", "system")
        idx = self.language.findData(current_language)
        self.language.setCurrentIndex(max(0, idx))
        lang_row.addWidget(self.language, 1)
        self.apply_language = QPushButton(owner.t("apply_restart"))
        self.apply_language.setProperty("secondary", True)
        self.apply_language.clicked.connect(owner.restart_for_language)
        lang_row.addWidget(self.apply_language)
        language_card.content.addLayout(lang_row)
        lay.addWidget(language_card)

        design = Card(owner.t("look"))
        g = QGridLayout()
        self.theme = QComboBox(); self.theme.addItems(THEMES.keys()); self.theme.setCurrentText(owner.settings["theme"])
        self.accent = QComboBox(); self.accent.addItems(ACCENTS.keys()); self.accent.setCurrentText(owner.settings["accent"])
        self.background = QComboBox(); self.background.addItems(BACKGROUND_NAMES); self.background.setCurrentText(owner.settings["background"])
        g.addWidget(QLabel(owner.t("theme")), 0, 0); g.addWidget(self.theme, 0, 1)
        g.addWidget(QLabel(owner.t("accent")), 1, 0); g.addWidget(self.accent, 1, 1)
        g.addWidget(QLabel(owner.t("background")), 2, 0); g.addWidget(self.background, 2, 1)
        design.content.addLayout(g)
        self.custom_bg = QPushButton(owner.t("custom_background"))
        self.custom_bg.setProperty("secondary", True)
        self.custom_bg.clicked.connect(self.choose_background)
        design.content.addWidget(self.custom_bg)
        lay.addWidget(design)

        motion = Card(owner.t("motion_quality"))
        mg = QGridLayout()
        self.animations = QCheckBox(owner.t("animations"))
        self.animations.setChecked(owner.settings["animations"])
        self.fps = QComboBox(); self.fps.addItems(["30", "60", "120", "160"]); self.fps.setCurrentText(str(owner.settings["background_fps"]))
        self.scale = QSlider(Qt.Horizontal); self.scale.setRange(80, 140); self.scale.setValue(owner.settings["ui_scale"])
        self.scale_label = QLabel(f'{owner.settings["ui_scale"]}%'); self.scale_label.setObjectName("muted")
        mg.addWidget(self.animations, 0, 0, 1, 2)
        mg.addWidget(QLabel(owner.t("background_fps")), 1, 0); mg.addWidget(self.fps, 1, 1)
        mg.addWidget(QLabel(owner.t("ui_size")), 2, 0)
        sr = QHBoxLayout(); sr.addWidget(self.scale, 1); sr.addWidget(self.scale_label); mg.addLayout(sr, 2, 1)
        motion.content.addLayout(mg)
        lay.addWidget(motion)

        self.smooth_scrolling = QCheckBox(owner.t("smooth_scrolling"))
        self.smooth_scrolling.setChecked(owner.settings.get("smooth_scrolling", True))
        motion.content.addWidget(self.smooth_scrolling)
        smooth_note = QLabel(owner.t("smooth_scrolling_note")); smooth_note.setWordWrap(True); smooth_note.setObjectName("muted")
        motion.content.addWidget(smooth_note)

        startup = Card(owner.t("start_screen"))
        sg = QGridLayout()
        self.startup_mode = QComboBox()
        self.startup_mode.addItem(owner.t("fullscreen"), "fullscreen")
        self.startup_mode.addItem(owner.t("compact"), "compact")
        self.startup_mode.addItem(owner.t("off"), "off")
        idx = self.startup_mode.findData(owner.settings["startup_screen"])
        self.startup_mode.setCurrentIndex(max(0, idx))
        self.startup_duration = QSpinBox(); self.startup_duration.setRange(400, 5000); self.startup_duration.setSuffix(" ms"); self.startup_duration.setValue(owner.settings["startup_duration_ms"])
        sg.addWidget(QLabel(owner.t("mode")), 0, 0); sg.addWidget(self.startup_mode, 0, 1)
        sg.addWidget(QLabel(owner.t("duration")), 1, 0); sg.addWidget(self.startup_duration, 1, 1)
        startup.content.addLayout(sg)
        note = QLabel(owner.t("startup_note"))
        note.setWordWrap(True); note.setObjectName("muted")
        startup.content.addWidget(note)
        self.setup_again = QPushButton("Open Setup Wizard")
        self.setup_again.setProperty("secondary", True)
        self.setup_again.clicked.connect(owner.open_setup_wizard)
        startup.content.addWidget(self.setup_again)
        lay.addWidget(startup)

        info = Card(owner.t("quality"))
        q = QLabel(owner.t("quality_note"))
        q.setWordWrap(True); q.setObjectName("muted")
        info.content.addWidget(q)
        lay.addWidget(info)
        lay.addStretch(1)

        self.scroll.setWidget(content)
        outer.addWidget(self.scroll, 1)
        self.scroll.verticalScrollBar().valueChanged.connect(owner._on_scroll_activity)

        for widget in [self.theme, self.accent, self.background, self.fps, self.startup_mode]:
            widget.currentIndexChanged.connect(self._changed)
        self.language.currentIndexChanged.connect(owner.schedule_save)
        self.animations.toggled.connect(self._changed)
        self.smooth_scrolling.toggled.connect(self._changed)
        self.scale.valueChanged.connect(self._scale_changed)
        self.startup_duration.valueChanged.connect(self._changed)

    def _scale_changed(self, value: int) -> None:
        self.scale_label.setText(f"{value}%")
        self._changed()

    def _changed(self, *_args) -> None:
        self.appearance_changed.emit()

    def values(self) -> dict:
        return {
            "theme": self.theme.currentText(),
            "accent": self.accent.currentText(),
            "background": self.background.currentText(),
            "background_fps": int(self.fps.currentText()),
            "animations": self.animations.isChecked(),
            "ui_scale": self.scale.value(),
            "startup_screen": self.startup_mode.currentData(),
            "startup_duration_ms": self.startup_duration.value(),
            "language": self.language.currentData(),
            "smooth_scrolling": self.smooth_scrolling.isChecked(),
        }


class AuralynWindow(QMainWindow):
    def __init__(self, settings: dict, lock_fd):
        super().__init__()
        self.settings = settings
        self.lock_fd = lock_fd
        self.worker: ClickWorker | None = None
        self.running = False
        self.total_clicks = 0
        self.last_clicks = 0
        self.last_stats_time = time.perf_counter()
        self.session_started = 0.0
        self.settings_open = False
        self._style_signature = None
        self.restart_requested = False

        self.scroll_resume_timer = QTimer(self)
        self.scroll_resume_timer.setSingleShot(True)
        self.scroll_resume_timer.setInterval(150)
        self.scroll_resume_timer.timeout.connect(self._resume_motion_after_scroll)

        self.resize_style_timer = QTimer(self)
        self.resize_style_timer.setSingleShot(True)
        self.resize_style_timer.setInterval(130)
        self.resize_style_timer.timeout.connect(self.apply_appearance)

        self.setWindowTitle(f"{APP_NAME} {__version__}")
        self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.resize(1240, 860)
        self.setMinimumSize(800, 620)

        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(220)
        self.save_timer.timeout.connect(self.save_current_settings)

        self.root = AnimatedBackground()
        self.root.setObjectName("root")
        self.setCentralWidget(self.root)
        self.root_layout = QVBoxLayout(self.root)
        self.root_layout.setContentsMargins(22, 18, 22, 20)
        self.root_layout.setSpacing(14)

        self._build_header()
        self._build_body()
        self.drawer = SettingsDrawer(self)
        self.drawer.appearance_changed.connect(self._on_appearance_changed)
        self.drawer.choose_background.connect(self._choose_custom_background)
        self.drawer.close_requested.connect(self.toggle_settings)
        self.drawer.hide()

        self._connect_autosave()
        self._install_shortcuts()
        self.apply_appearance()

        self.stats_timer = QTimer(self)
        self.stats_timer.setInterval(50)
        self.stats_timer.timeout.connect(self._update_stats)
        self.stats_timer.start()

    def t(self, key: str, **kwargs) -> str:
        return tr(self.settings.get("language", "system"), key, **kwargs)

    def restart_for_language(self) -> None:
        self.settings.update(self.drawer.values())
        self.save_current_settings()
        self.restart_requested = True
        self.close()

    def open_setup_wizard(self) -> None:
        self.settings.update(self.drawer.values())
        self.save_current_settings()
        wizard = SetupWizard(dict(self.settings), self)
        if wizard.exec():
            self.settings = load_settings()
            self.restart_requested = True
            self.close()

    def _build_header(self) -> None:
        header = QHBoxLayout()
        header.setSpacing(12)
        logo = QLabel()
        logo.setPixmap(QIcon(str(ICON_PATH)).pixmap(54, 54))
        logo.setFixedSize(58, 58)
        header.addWidget(logo)

        titles = QVBoxLayout(); titles.setSpacing(0)
        title = QLabel(APP_NAME); title.setObjectName("appTitle")
        subtitle = QLabel(f"v{__version__} • {self.t("app_subtitle")}"); subtitle.setObjectName("muted")
        titles.addWidget(title); titles.addWidget(subtitle)
        header.addLayout(titles)
        header.addStretch(1)

        self.status = QLabel(f"●  {self.t("status_ready")}"); self.status.setObjectName("statusBadge")
        header.addWidget(self.status)
        self.gear = QPushButton("⚙")
        self.gear.setObjectName("gearButton")
        self.gear.setToolTip(self.t("display_design"))
        self.gear.setFixedWidth(52)
        self.gear.clicked.connect(self.toggle_settings)
        header.addWidget(self.gear)
        self.root_layout.addLayout(header)

    def _build_body(self) -> None:
        self.scroll = QScrollArea()
        self.scroll.setObjectName("mainScroll")
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.body_widget = QWidget(); self.body_widget.setObjectName("transparent")
        self.body = QBoxLayout(QBoxLayout.LeftToRight, self.body_widget)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(15)
        self.scroll.setWidget(self.body_widget)
        self.root_layout.addWidget(self.scroll, 1)
        self.scroll.verticalScrollBar().valueChanged.connect(self._on_scroll_activity)

        self.left = QWidget(); self.left.setObjectName("transparent")
        left = QVBoxLayout(self.left); left.setContentsMargins(0, 0, 0, 0); left.setSpacing(14)
        self._build_timing(left)
        self._build_click_settings(left)
        self._build_session(left)
        self._build_position(left)
        self._build_burst(left)
        left.addStretch(1)

        self.right = QWidget(); self.right.setObjectName("transparent"); self.right.setMinimumWidth(315)
        right = QVBoxLayout(self.right); right.setContentsMargins(0, 0, 0, 0); right.setSpacing(14)
        self._build_live(right)
        self._build_presets(right)
        self._build_hotkeys(right)
        right.addStretch(1)

        self.body.addWidget(self.left, 7)
        self.body.addWidget(self.right, 3)

    def _spin(self, low: int, high: int, value: int, suffix: str = "") -> QSpinBox:
        box = QSpinBox(); box.setRange(low, high); box.setValue(value); box.setSuffix(suffix)
        return box

    def _build_timing(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("timing"), self.t("timing_subtitle"))
        self.timing_mode = SegmentControl([(self.t("interval"), "interval"), (self.t("cps"), "cps")], self.settings["timing_mode"])
        card.content.addWidget(self.timing_mode)

        self.interval_panel = QWidget(); self.interval_panel.setObjectName("transparent")
        grid = QGridLayout(self.interval_panel); grid.setContentsMargins(0, 0, 0, 0); grid.setHorizontalSpacing(9)
        self.hours = self._spin(0, 99, self.settings["hours"])
        self.minutes = self._spin(0, 59, self.settings["minutes"])
        self.seconds = self._spin(0, 59, self.settings["seconds"])
        self.millis = self._spin(0, 999, self.settings["millis"])
        for col, (name, widget) in enumerate([(self.t("hours"), self.hours), (self.t("minutes"), self.minutes), (self.t("seconds"), self.seconds), (self.t("milliseconds"), self.millis)]):
            lab = QLabel(name); lab.setObjectName("fieldLabel"); grid.addWidget(lab, 0, col); grid.addWidget(widget, 1, col)
        card.content.addWidget(self.interval_panel)

        self.cps_panel = QWidget(); self.cps_panel.setObjectName("transparent")
        cps_row = QHBoxLayout(self.cps_panel); cps_row.setContentsMargins(0, 0, 0, 0)
        cps_row.addWidget(QLabel(self.t("target_cps")))
        self.cps = self._spin(1, 1000, self.settings["cps"], " CPS")
        cps_row.addWidget(self.cps, 1)
        card.content.addWidget(self.cps_panel)

        presets = QHBoxLayout(); presets.setSpacing(7)
        for text, ms in [("1 ms", 1), ("5 ms", 5), ("10 ms", 10), ("50 ms", 50), ("100 ms", 100)]:
            btn = QPushButton(text); btn.setProperty("chip", True); btn.clicked.connect(lambda _=False, v=ms: self._set_interval_preset(v)); presets.addWidget(btn)
        presets.addStretch(1); card.content.addLayout(presets)
        layout.addWidget(card)
        self.timing_mode.changed.connect(self._sync_timing_panels)
        self._sync_timing_panels()

    def _build_click_settings(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("click_style"))
        row = QHBoxLayout(); row.setSpacing(12)
        a = QVBoxLayout(); lab = QLabel(self.t("mouse_button")); lab.setObjectName("fieldLabel"); a.addWidget(lab)
        self.mouse_seg = SegmentControl([(self.t("left"), "left"), (self.t("right"), "right"), (self.t("middle"), "middle")], self.settings["button"]); a.addWidget(self.mouse_seg)
        b = QVBoxLayout(); lab2 = QLabel(self.t("click_type")); lab2.setObjectName("fieldLabel"); b.addWidget(lab2)
        self.type_seg = SegmentControl([("1×", "single"), ("2×", "double"), ("3×", "triple")], self.settings["click_type"]); b.addWidget(self.type_seg)
        row.addLayout(a, 1); row.addLayout(b, 1); card.content.addLayout(row)

        press = QHBoxLayout(); press.addWidget(QLabel(self.t("hold_per_click"))); self.press_duration = self._spin(0, 10000, self.settings["press_duration_ms"], " ms"); press.addWidget(self.press_duration); card.content.addLayout(press)
        layout.addWidget(card)

    def _build_session(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("session"), self.t("session_subtitle"))
        self.infinite = QCheckBox(self.t("infinite"))
        self.infinite.setChecked(self.settings["repeat_mode"] == "infinite")
        self.repeat_count = self._spin(1, 999_999_999, self.settings["repeat_count"])
        r = QHBoxLayout(); r.addWidget(self.infinite, 1); r.addWidget(QLabel(self.t("actions"))); r.addWidget(self.repeat_count); card.content.addLayout(r)

        delay = QHBoxLayout(); delay.addWidget(QLabel(self.t("start_delay"))); self.start_delay = self._spin(0, 60000, self.settings["start_delay_ms"], " ms"); delay.addWidget(self.start_delay, 1); card.content.addLayout(delay)

        self.time_limit_enabled = QCheckBox(self.t("time_limit"))
        self.time_limit_enabled.setChecked(self.settings["time_limit_enabled"])
        self.time_limit = self._spin(1, 86400, self.settings["time_limit_seconds"], " s")
        t = QHBoxLayout(); t.addWidget(self.time_limit_enabled, 1); t.addWidget(self.time_limit); card.content.addLayout(t)
        layout.addWidget(card)

    def _build_position(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("position_randomness"))
        self.fixed = QCheckBox(self.t("fixed_position"))
        self.fixed.setChecked(self.settings["position_mode"] == "fixed")
        self.pos_x = self._spin(-99999, 99999, self.settings["pos_x"])
        self.pos_y = self._spin(-99999, 99999, self.settings["pos_y"])
        capture = QPushButton(self.t("capture_position")); capture.setProperty("secondary", True); capture.clicked.connect(self.capture_position)
        p = QHBoxLayout(); p.addWidget(self.fixed); p.addWidget(QLabel("X")); p.addWidget(self.pos_x); p.addWidget(QLabel("Y")); p.addWidget(self.pos_y); p.addWidget(capture, 1); card.content.addLayout(p)

        self.random_delay = QCheckBox(self.t("random_delay"))
        self.random_delay.setChecked(self.settings["random_delay"])
        self.random_delay_ms = self._spin(0, 10000, self.settings["random_delay_ms"], " ms")
        rd = QHBoxLayout(); rd.addWidget(self.random_delay, 1); rd.addWidget(self.random_delay_ms); card.content.addLayout(rd)

        self.random_position = QCheckBox(self.t("random_radius"))
        self.random_position.setChecked(self.settings["random_position"])
        self.random_radius = self._spin(0, 1000, self.settings["random_position_radius"], " px")
        rp = QHBoxLayout(); rp.addWidget(self.random_position, 1); rp.addWidget(self.random_radius); card.content.addLayout(rp)
        layout.addWidget(card)

    def _build_burst(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("burst_mode"), self.t("burst_subtitle"))
        self.burst = QCheckBox(self.t("burst_active"))
        self.burst.setChecked(self.settings["burst_enabled"])
        self.burst_count = self._spin(1, 100000, self.settings["burst_count"])
        self.burst_pause = self._spin(0, 60000, self.settings["burst_pause_ms"], " ms")
        row = QHBoxLayout(); row.addWidget(self.burst); row.addWidget(QLabel(self.t("actions"))); row.addWidget(self.burst_count, 1); row.addWidget(QLabel(self.t("pause"))); row.addWidget(self.burst_pause, 1); card.content.addLayout(row)
        layout.addWidget(card)

    def _build_live(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("live_control"))
        self.orb = LiveOrb()
        row = QHBoxLayout(); row.addStretch(1); row.addWidget(self.orb); row.addStretch(1); card.content.addLayout(row)
        self.start_btn = QPushButton(self.t("start")); self.start_btn.setObjectName("startButton"); self.start_btn.clicked.connect(self.toggle); card.content.addWidget(self.start_btn)
        self.stop_btn = QPushButton(self.t("stop_emergency")); self.stop_btn.setObjectName("dangerButton"); self.stop_btn.clicked.connect(self.stop_clicking); card.content.addWidget(self.stop_btn)

        grid = QGridLayout()
        self.cps_live = QLabel("0.0"); self.cps_live.setObjectName("bigStat")
        self.clicks_live = QLabel("0"); self.clicks_live.setObjectName("bigStat")
        self.elapsed_live = QLabel("0.0s"); self.elapsed_live.setObjectName("bigStatSmall")
        for col, (widget, label) in enumerate([(self.cps_live, self.t("cps")), (self.clicks_live, self.t("clicks")), (self.elapsed_live, self.t("time"))]):
            grid.addWidget(widget, 0, col); cap = QLabel(label); cap.setObjectName("muted"); grid.addWidget(cap, 1, col)
        card.content.addLayout(grid)
        layout.addWidget(card)

    def _build_presets(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("quick_presets"))
        for text, mode, value in [
            ("Smooth • 10 CPS", "cps", 10),
            ("Fast • 20 CPS", "cps", 20),
            ("Turbo • 100 CPS", "cps", 100),
            ("1 ms • Maximum", "interval", 1),
        ]:
            b = QPushButton(text); b.setProperty("preset", True); b.clicked.connect(lambda _=False, m=mode, v=value: self._apply_quick_preset(m, v)); card.content.addWidget(b)
        layout.addWidget(card)

    def _build_hotkeys(self, layout: QVBoxLayout) -> None:
        card = Card(self.t("global_hotkeys"))
        for text in [self.t("hk_start_stop"), self.t("hk_position"), self.t("hk_stop")]:
            lab = QLabel(text); lab.setObjectName("hotkey"); card.content.addWidget(lab)
        layout.addWidget(card)

    def _connect_autosave(self) -> None:
        for w in [self.hours, self.minutes, self.seconds, self.millis, self.cps, self.press_duration, self.repeat_count, self.start_delay, self.time_limit, self.pos_x, self.pos_y, self.random_delay_ms, self.random_radius, self.burst_count, self.burst_pause]:
            w.valueChanged.connect(self.schedule_save)
        for w in [self.infinite, self.time_limit_enabled, self.fixed, self.random_delay, self.random_position, self.burst]:
            w.toggled.connect(self.schedule_save)
        for w in [self.timing_mode, self.mouse_seg, self.type_seg]:
            w.changed.connect(self.schedule_save)

    def _install_shortcuts(self) -> None:
        QShortcut(QKeySequence("F6"), self, activated=self.toggle)
        QShortcut(QKeySequence("F7"), self, activated=self.capture_position)
        QShortcut(QKeySequence("F8"), self, activated=self.stop_clicking)

    def _sync_timing_panels(self, *_args) -> None:
        interval = self.timing_mode.value() == "interval"
        self.interval_panel.setVisible(interval)
        self.cps_panel.setVisible(not interval)
        self.schedule_save()

    def _set_interval_preset(self, ms: int) -> None:
        self.timing_mode.set_value("interval", True)
        self.hours.setValue(0); self.minutes.setValue(0); self.seconds.setValue(0); self.millis.setValue(ms)

    def _apply_quick_preset(self, mode: str, value: int) -> None:
        self.timing_mode.set_value(mode, True)
        if mode == "cps":
            self.cps.setValue(value)
        else:
            self.hours.setValue(0); self.minutes.setValue(0); self.seconds.setValue(0); self.millis.setValue(value)
        self.status.setText(f"●  {self.t("status_preset")}")

    def schedule_save(self, *_args) -> None:
        self.save_timer.start()

    def collect_settings(self) -> dict:
        data = dict(self.settings)
        data.update({
            "timing_mode": self.timing_mode.value(),
            "hours": self.hours.value(), "minutes": self.minutes.value(), "seconds": self.seconds.value(), "millis": self.millis.value(), "cps": self.cps.value(),
            "button": self.mouse_seg.value(), "click_type": self.type_seg.value(),
            "repeat_mode": "infinite" if self.infinite.isChecked() else "count", "repeat_count": self.repeat_count.value(),
            "position_mode": "fixed" if self.fixed.isChecked() else "current", "pos_x": self.pos_x.value(), "pos_y": self.pos_y.value(),
            "random_delay": self.random_delay.isChecked(), "random_delay_ms": self.random_delay_ms.value(),
            "random_position": self.random_position.isChecked(), "random_position_radius": self.random_radius.value(),
            "press_duration_ms": self.press_duration.value(), "start_delay_ms": self.start_delay.value(),
            "burst_enabled": self.burst.isChecked(), "burst_count": self.burst_count.value(), "burst_pause_ms": self.burst_pause.value(),
            "time_limit_enabled": self.time_limit_enabled.isChecked(), "time_limit_seconds": self.time_limit.value(),
        })
        if hasattr(self, "drawer"):
            data.update(self.drawer.values())
        return data

    def save_current_settings(self) -> None:
        try:
            self.settings = self.collect_settings()
            save_settings(self.settings)
        except Exception as exc:
            print("Auralyn Click settings save failed:", exc)

    def _on_appearance_changed(self) -> None:
        self.settings.update(self.drawer.values())
        self.apply_appearance()
        self.schedule_save()

    def _choose_custom_background(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(self, self.t("custom_dialog"), str(Path.home()), self.t("custom_dialog_filter"))
        if not filename:
            return
        stored = import_custom_background(filename)
        if stored:
            self.settings["custom_background"] = stored
            self.drawer.background.setCurrentText("Custom")
            self.apply_appearance()
            self.schedule_save()

    def apply_appearance(self) -> None:
        pal = THEMES.get(self.drawer.theme.currentText(), THEMES["Midnight"])
        accent = ACCENTS.get(self.drawer.accent.currentText(), ACCENTS["Violet"])
        fps = int(self.drawer.fps.currentText())
        animations = self.drawer.animations.isChecked()
        background = self.drawer.background.currentText()
        self.root.configure(mode=background, theme_bg=pal["bg"], accent=accent, animations=animations, fps=fps, custom_path=self.settings.get("custom_background", ""))

        wf = min(max(0.75, self.width() / 1240), max(0.75, self.height() / 860))
        scale = max(0.72, min(1.55, wf * (self.drawer.scale.value() / 100.0)))
        fs = max(10, round(14 * scale)); sm = max(9, round(12 * scale)); title = max(26, round(36 * scale)); card_title = max(14, round(17 * scale)); h = max(36, round(45 * scale)); rad = max(10, round(16 * scale)); pad = max(8, round(12 * scale))
        panel = rgba(pal["panel"], 228 if background != "Static Gradient" else 245)
        panel2 = rgba(pal["panel2"], 235)
        panel3 = rgba(pal["panel3"], 240)

        # Avoid rebuilding the full Qt stylesheet when a resize only changes a
        # few pixels. Re-polishing the whole widget tree is expensive.
        style_signature = (
            self.drawer.theme.currentText(),
            self.drawer.accent.currentText(),
            background,
            round(scale, 2),
            animations,
        )
        if style_signature == self._style_signature:
            return
        self._style_signature = style_signature

        self.setStyleSheet(f'''
        QWidget#transparent{{background:transparent;}}
        QWidget{{color:{pal['text']};font-family:Inter,"Noto Sans",Ubuntu,Sans;font-size:{fs}px;}}
        QLabel#appTitle{{font-size:{title}px;font-weight:900;}}
        QLabel#muted{{color:{pal['muted']};font-size:{sm}px;}}
        QLabel#fieldLabel{{color:{pal['muted']};font-size:{sm}px;font-weight:700;}}
        QFrame#card{{background:{panel};border:1px solid {rgba(pal['border'],220)};border-radius:{rad}px;}}
        QLabel#cardTitle{{font-size:{card_title}px;font-weight:900;}}
        QLabel#statusBadge{{background:{panel2};border:1px solid {rgba(pal['border'],220)};border-radius:{max(12,round(18*scale))}px;padding:{max(6,round(8*scale))}px {max(10,round(14*scale))}px;font-weight:900;color:{pal['success']};}}
        QPushButton{{min-height:{h}px;background:{panel2};border:1px solid {rgba(pal['border'],230)};border-radius:{max(8,round(11*scale))}px;padding:0 {pad}px;font-weight:750;}}
        QPushButton:hover{{background:{panel3};border-color:{accent};}}
        QPushButton:pressed{{background:{accent};color:white;}}
        QPushButton#gearButton,QPushButton#iconButton{{font-size:{max(17,round(22*scale))}px;}}
        QPushButton#startButton{{min-height:{max(54,round(64*scale))}px;background:{accent};color:white;border:none;border-radius:{max(11,round(15*scale))}px;font-size:{max(14,round(17*scale))}px;font-weight:950;}}
        QPushButton#dangerButton{{min-height:{max(44,round(52*scale))}px;background:{rgba(pal['danger'],20)};color:{pal['danger']};border:1px solid {pal['danger']};font-weight:900;}}
        QPushButton#dangerButton:hover{{background:{pal['danger']};color:white;}}
        QPushButton[chip="true"]{{min-height:{max(30,round(34*scale))}px;border-radius:{max(10,round(17*scale))}px;color:{pal['muted']};font-size:{sm}px;}}
        QPushButton[preset="true"]{{text-align:left;padding-left:{max(12,round(16*scale))}px;}}
        QPushButton[secondary="true"]{{color:{accent};}}
        QSpinBox,QComboBox{{min-height:{h}px;background:{panel2};border:1px solid {rgba(pal['border'],230)};border-radius:{max(8,round(11*scale))}px;padding:0 {pad}px;selection-background-color:{accent};}}
        QSpinBox:focus,QComboBox:focus{{border:1px solid {accent};}}
        QComboBox QAbstractItemView{{background:{pal['panel2']};color:{pal['text']};selection-background-color:{accent};border:1px solid {pal['border']};}}
        QCheckBox::indicator{{width:{max(18,round(22*scale))}px;height:{max(18,round(22*scale))}px;border:1px solid {pal['border']};border-radius:{max(4,round(6*scale))}px;background:{panel2};}}
        QCheckBox::indicator:checked{{background:{accent};border-color:{accent};}}
        QWidget#segmentWrap{{background:{panel2};border:1px solid {rgba(pal['border'],230)};border-radius:{max(10,round(13*scale))}px;}}
        QFrame#segmentIndicator{{background:{accent};border-radius:{max(8,round(10*scale))}px;}}
        QPushButton[segment="true"]{{min-height:{h}px;background:transparent;border:none;color:{pal['muted']};font-weight:850;}}
        QPushButton[segment="true"]:checked{{color:white;}}
        QLabel#bigStat{{font-size:{max(24,round(34*scale))}px;font-weight:950;color:{accent};}}
        QLabel#bigStatSmall{{font-size:{max(18,round(24*scale))}px;font-weight:900;color:{accent};}}
        QLabel#hotkey{{background:{panel2};border:1px solid {rgba(pal['border'],220)};border-radius:{max(8,round(10*scale))}px;padding:{max(8,round(10*scale))}px {pad}px;font-weight:800;}}
        QScrollArea#mainScroll{{border:none;background:transparent;}}
        QScrollArea#mainScroll>QWidget>QWidget{{background:transparent;}}
        QScrollBar:vertical{{width:{max(8,round(10*scale))}px;background:transparent;}}
        QScrollBar::handle:vertical{{background:{rgba(pal['panel3'],210)};border-radius:4px;min-height:40px;}}
        QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}
        QFrame#settingsDrawer{{background:{rgba(pal['panel'],248)};border:1px solid {rgba(pal['border'],235)};border-radius:{max(14,round(20*scale))}px;}}
        QLabel#drawerTitle{{font-size:{max(20,round(26*scale))}px;font-weight:950;}}
        QSlider::groove:horizontal{{height:{max(4,round(6*scale))}px;background:{pal['panel3']};border-radius:3px;}}
        QSlider::sub-page:horizontal{{background:{accent};border-radius:3px;}}
        QSlider::handle:horizontal{{width:{max(14,round(18*scale))}px;margin:-6px 0;border-radius:{max(7,round(9*scale))}px;background:{accent};}}
        ''')

        for segment in [self.timing_mode, self.mouse_seg, self.type_seg]:
            segment.animations = animations
        self.orb.set_state(self.running, animations, accent)
        self._set_glow(self.running)

    def _set_glow(self, active: bool) -> None:
        if not active or not self.drawer.animations.isChecked():
            self.start_btn.setGraphicsEffect(None)
            return
        effect = QGraphicsDropShadowEffect(self.start_btn)
        effect.setColor(QColor(ACCENTS[self.drawer.accent.currentText()]))
        effect.setBlurRadius(28)
        effect.setOffset(0, 0)
        self.start_btn.setGraphicsEffect(effect)
        self._glow_anim = QPropertyAnimation(effect, b"blurRadius", self)
        self._glow_anim.setDuration(950)
        self._glow_anim.setStartValue(18.0)
        self._glow_anim.setEndValue(42.0)
        self._glow_anim.setEasingCurve(QEasingCurve.InOutSine)
        self._glow_anim.setLoopCount(-1)
        self._glow_anim.start()

    def _on_scroll_activity(self, *_args) -> None:
        smooth = self.drawer.smooth_scrolling.isChecked() if hasattr(self, "drawer") else self.settings.get("smooth_scrolling", True)
        if not smooth:
            return
        self.root.set_interaction_paused(True)
        if hasattr(self, "orb"):
            self.orb.set_interaction_paused(True)
        if hasattr(self, "_glow_anim") and self._glow_anim is not None:
            try:
                self._glow_anim.pause()
            except Exception:
                pass
        self.scroll_resume_timer.start()

    def _resume_motion_after_scroll(self) -> None:
        self.root.set_interaction_paused(False)
        if hasattr(self, "orb"):
            self.orb.set_interaction_paused(False)
        if hasattr(self, "_glow_anim") and self._glow_anim is not None:
            try:
                self._glow_anim.resume()
            except Exception:
                pass

    def toggle_settings(self) -> None:
        opening = not self.settings_open
        self.settings_open = opening
        width = min(450, max(360, round(self.width() * 0.36)))
        h = max(100, self.root.height() - 16)
        offscreen = QRect(self.root.width() + 6, 8, width, h)
        onscreen = QRect(self.root.width() - width - 8, 8, width, h)
        if opening:
            self.drawer.setGeometry(offscreen)
            self.drawer.show(); self.drawer.raise_()
            start, end = offscreen, onscreen
        else:
            start, end = self.drawer.geometry(), offscreen
        if not self.drawer.animations.isChecked():
            self.drawer.setGeometry(end)
            if not self.settings_open:
                self.drawer.hide()
            return
        self._drawer_anim = QPropertyAnimation(self.drawer, b"geometry", self)
        self._drawer_anim.setDuration(260)
        self._drawer_anim.setStartValue(start)
        self._drawer_anim.setEndValue(end)
        self._drawer_anim.setEasingCurve(QEasingCurve.OutCubic)
        if not self.settings_open:
            self._drawer_anim.finished.connect(self.drawer.hide)
        self._drawer_anim.start()

    def show_with_animation(self) -> None:
        self.show()
        self.raise_()
        self.activateWindow()
        self._animate_window_in()

    def _animate_window_in(self) -> None:
        if not self.settings.get("animations", True):
            return
        target = self.geometry()
        start = QRect(target.x() + round(target.width()*0.025), target.y() + round(target.height()*0.025), round(target.width()*0.95), round(target.height()*0.95))
        self.setGeometry(start)
        self._window_anim = QPropertyAnimation(self, b"geometry", self)
        self._window_anim.setDuration(320)
        self._window_anim.setStartValue(start)
        self._window_anim.setEndValue(target)
        self._window_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._window_anim.start()

        opacity = QGraphicsOpacityEffect(self.centralWidget())
        self.centralWidget().setGraphicsEffect(opacity)
        self._fade_in = QPropertyAnimation(opacity, b"opacity", self)
        self._fade_in.setDuration(320); self._fade_in.setStartValue(0.0); self._fade_in.setEndValue(1.0)
        self._fade_in.finished.connect(lambda: self.centralWidget().setGraphicsEffect(None))
        self._fade_in.start()

    def interval_seconds(self) -> float:
        if self.timing_mode.value() == "cps":
            return max(0.001, 1.0 / max(1, self.cps.value()))
        return max(0.001, self.hours.value()*3600 + self.minutes.value()*60 + self.seconds.value() + self.millis.value()/1000.0)

    def build_config(self) -> ClickConfig:
        return ClickConfig(
            interval=self.interval_seconds(),
            button=self.mouse_seg.value(),
            click_type=self.type_seg.value(),
            repeat_mode="infinite" if self.infinite.isChecked() else "count",
            repeat_count=self.repeat_count.value(),
            position_mode="fixed" if self.fixed.isChecked() else "current",
            pos_x=self.pos_x.value(), pos_y=self.pos_y.value(),
            random_delay=self.random_delay.isChecked(), random_delay_ms=self.random_delay_ms.value(),
            random_position=self.random_position.isChecked(), random_position_radius=self.random_radius.value(),
            press_duration_ms=self.press_duration.value(), start_delay_ms=self.start_delay.value(),
            burst_enabled=self.burst.isChecked(), burst_count=self.burst_count.value(), burst_pause_ms=self.burst_pause.value(),
            time_limit_enabled=self.time_limit_enabled.isChecked(), time_limit_seconds=self.time_limit.value(),
        )

    def toggle(self) -> None:
        self.stop_clicking() if self.running else self.start_clicking()

    def start_clicking(self) -> None:
        if self.running:
            return
        self.save_current_settings()
        self.total_clicks = 0; self.last_clicks = 0; self.last_stats_time = time.perf_counter(); self.session_started = time.perf_counter()
        self.running = True
        self.worker = ClickWorker(self.build_config())
        self.worker.count_changed.connect(self._on_count)
        self.worker.state_text.connect(lambda text: self.status.setText(f"●  {text.upper()}"))
        self.worker.errored.connect(self._on_error)
        self.worker.done.connect(self._on_done)
        self.worker.start()
        self.start_btn.setText(self.t("stop_toggle")); self.status.setText(f"●  {self.t("status_active")}")
        self.orb.set_state(True, self.drawer.animations.isChecked(), ACCENTS[self.drawer.accent.currentText()]); self._set_glow(True)

    def stop_clicking(self) -> None:
        if self.worker and self.worker.isRunning():
            self.worker.stop()
        self.running = False
        self.start_btn.setText(self.t("start")); self.status.setText(f"●  {self.t("status_stopped")}")
        self.orb.set_state(False, self.drawer.animations.isChecked(), ACCENTS[self.drawer.accent.currentText()]); self._set_glow(False)

    def _on_count(self, count: int) -> None:
        self.total_clicks = count

    def _on_error(self, message: str) -> None:
        print("Auralyn Click worker error:", message)
        self.stop_clicking(); self.status.setText(f"●  {self.t("status_error")}")

    def _on_done(self) -> None:
        if self.running:
            self.running = False; self.start_btn.setText(self.t("start")); self.status.setText(f"●  {self.t("status_finished")}")
            self.orb.set_state(False, self.drawer.animations.isChecked(), ACCENTS[self.drawer.accent.currentText()]); self._set_glow(False)
        self.worker = None

    def _update_stats(self) -> None:
        now = time.perf_counter(); dt = now - self.last_stats_time
        if dt >= 0.25:
            cps = (self.total_clicks - self.last_clicks) / dt if dt > 0 else 0.0
            self.cps_live.setText(f"{cps:.1f}"); self.last_clicks = self.total_clicks; self.last_stats_time = now
        self.clicks_live.setText(str(self.total_clicks))
        elapsed = now - self.session_started if self.session_started else 0.0
        self.elapsed_live.setText(f"{elapsed:.1f}s")

    def capture_position(self) -> None:
        try:
            x, y = mouse.Controller().position
            self.pos_x.setValue(int(x)); self.pos_y.setValue(int(y)); self.fixed.setChecked(True)
            self.status.setText(f"●  POSITION {int(x)}, {int(y)}")
            self.schedule_save()
        except Exception as exc:
            print("Position capture failed:", exc)

    def handle_command(self, command: str) -> None:
        if command == "toggle": self.toggle()
        elif command == "start": self.start_clicking()
        elif command == "stop": self.stop_clicking()
        elif command == "capture": self.capture_position()
        elif command == "show": self.show_window()

    def show_window(self) -> None:
        if self.isMinimized(): self.showNormal()
        self.show(); self.raise_(); self.activateWindow()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "body"):
            if self.width() < 930 and self.body.direction() != QBoxLayout.TopToBottom:
                self.body.setDirection(QBoxLayout.TopToBottom); self.right.setMinimumWidth(0)
            elif self.width() >= 930 and self.body.direction() != QBoxLayout.LeftToRight:
                self.body.setDirection(QBoxLayout.LeftToRight); self.right.setMinimumWidth(315)
        if hasattr(self, "drawer") and self.drawer.isVisible():
            width = min(450, max(360, round(self.width() * 0.36))); h = max(100, self.root.height() - 16)
            x = self.root.width() - width - 8 if self.settings_open else self.root.width() + 6
            self.drawer.setGeometry(QRect(x, 8, width, h))
        self.resize_style_timer.start()

    def closeEvent(self, event) -> None:
        self.stop_clicking(); self.save_current_settings()
        release_single_instance(self.lock_fd)
        event.accept()


def main() -> None:
    command_map = {
        "--toggle": "toggle",
        "--start": "start",
        "--stop": "stop",
        "--capture": "capture",
        "--show": "show",
    }
    pending_command = next((command_map[a] for a in sys.argv[1:] if a in command_map), None)
    force_setup = "--setup" in sys.argv[1:]
    if pending_command is not None:
        if send_command(pending_command, retries=1):
            return
        # Emergency stop and position capture must never launch a new app.
        if pending_command in {"stop", "capture"}:
            return

    lock_fd = acquire_single_instance()
    if lock_fd is None:
        send_command("show", retries=20)
        return

    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Julius.AuralynClick")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName("AuralynClick")
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName("Julius")
    app.setOrganizationDomain("auralyn-click.local")
    app.setWindowIcon(QIcon(str(ICON_PATH)))
    if not sys.platform.startswith("win"):
        QGuiApplication.setDesktopFileName(APP_SLUG)

    settings = load_settings()
    if force_setup or not settings.get("setup_completed", False):
        wizard = SetupWizard(settings)
        wizard.exec()
        settings = load_settings()
    app.setLayoutDirection(Qt.RightToLeft if resolve_language(settings.get("language", "system")) == "ar" else Qt.LeftToRight)
    window = AuralynWindow(settings, lock_fd)

    bridge = IPCBridge()
    server = IPCServer(bridge)
    bridge.command.connect(window.handle_command)
    server.start()

    ensure_linux_global_hotkeys()

    # Windows does not have GNOME custom shortcuts, so register the global
    # F6/F7/F8 keys directly with pynput. Callbacks emit into Qt safely.
    global_hotkeys = None
    if sys.platform.startswith("win"):
        try:
            global_hotkeys = keyboard.GlobalHotKeys({
                "<f6>": lambda: bridge.command.emit("toggle"),
                "<f7>": lambda: bridge.command.emit("capture"),
                "<f8>": lambda: bridge.command.emit("stop"),
            })
            global_hotkeys.start()
        except Exception as exc:
            print("Auralyn Click global hotkeys failed:", exc)

    if pending_command in {"toggle", "start"}:
        QTimer.singleShot(250, lambda command=pending_command: window.handle_command(command))

    splash = None
    if settings["startup_screen"] != "off":
        splash = SplashScreen(settings)
        splash.finished.connect(window.show_with_animation)
    else:
        window.show_with_animation()

    rc = app.exec()
    restart_requested = bool(getattr(window, "restart_requested", False))
    server.stop()
    if global_hotkeys is not None:
        try:
            global_hotkeys.stop()
        except Exception:
            pass
    if restart_requested:
        try:
            subprocess.Popen(
                _launch_command(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception as exc:
            print("Auralyn Click restart failed:", exc)
    sys.exit(rc)


if __name__ == "__main__":
    main()
