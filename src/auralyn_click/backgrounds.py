from __future__ import annotations

import math
import random
import time
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import (
    QColor,
    QLinearGradient,
    QMovie,
    QPainter,
    QPen,
    QPixmap,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget


class AnimatedBackground(QWidget):
    """Procedural background renderer with scroll-aware performance controls.

    The expensive background animation is deliberately paused while the user is
    actively scrolling. This prevents the animated central widget and the
    transparent scroll viewport from competing for the same paint budget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = "Aurora"
        self.theme_bg = QColor("#0B0D12")
        self.accent = QColor("#7C5CFF")
        self.secondary = QColor("#35D39A")
        self.animations = True
        self.fps = 60
        self.custom_path = ""
        self.interaction_paused = False

        self.custom_pixmap = QPixmap()
        self.custom_scaled = QPixmap()
        self.custom_movie: QMovie | None = None
        self._custom_cache_size = QSize()

        self.t0 = time.perf_counter()
        rng = random.Random(34119)
        self.stars = [
            (rng.random(), rng.random(), rng.uniform(0.5, 2.2), rng.random())
            for _ in range(72)
        ]
        self.particles = [
            (rng.random(), rng.random(), rng.uniform(0.03, 0.12), rng.uniform(1.0, 3.4))
            for _ in range(54)
        ]

        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self.update)

        # We always paint every pixel of the background.
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAutoFillBackground(False)
        self._sync_timer()

    def configure(
        self,
        *,
        mode: str,
        theme_bg: str,
        accent: str,
        animations: bool,
        fps: int,
        custom_path: str = "",
    ) -> None:
        changed_custom = custom_path != self.custom_path or mode != self.mode
        self.mode = mode
        self.theme_bg = QColor(theme_bg)
        self.accent = QColor(accent)
        self.secondary = self._shift_hue(self.accent, 115)
        self.animations = animations
        self.fps = max(1, int(fps))
        self.custom_path = custom_path
        if changed_custom:
            self._load_custom()
        self._sync_timer()
        self.update()

    def set_interaction_paused(self, paused: bool) -> None:
        if self.interaction_paused == paused:
            return
        self.interaction_paused = paused
        self._sync_timer()
        if not paused:
            self.update()

    @staticmethod
    def _shift_hue(color: QColor, degrees: int) -> QColor:
        h, s, v, a = color.getHsv()
        if h < 0:
            h = 0
        out = QColor()
        out.setHsv((h + degrees) % 360, max(120, s), max(150, v), a)
        return out

    def _sync_timer(self) -> None:
        procedural = self.mode not in {"Static Gradient", "Custom"}
        should_run = self.animations and procedural and not self.interaction_paused and self.isVisible()

        if should_run:
            interval = max(6, round(1000 / max(1, self.fps)))
            if self.timer.interval() != interval:
                self.timer.setInterval(interval)
            if not self.timer.isActive():
                self.timer.start()
        else:
            self.timer.stop()

        if self.custom_movie:
            # QMovie has its own timer. Do not also run the procedural timer.
            paused = (not self.animations) or self.interaction_paused or not self.isVisible()
            self.custom_movie.setPaused(paused)

    def _load_custom(self) -> None:
        if self.custom_movie:
            try:
                self.custom_movie.stop()
                self.custom_movie.frameChanged.disconnect(self._on_movie_frame)
            except Exception:
                pass
            self.custom_movie = None

        self.custom_pixmap = QPixmap()
        self.custom_scaled = QPixmap()
        self._custom_cache_size = QSize()

        path = Path(self.custom_path)
        if self.mode != "Custom" or not path.is_file():
            return

        if path.suffix.lower() == ".gif":
            movie = QMovie(str(path))
            movie.setCacheMode(QMovie.CacheAll)
            if movie.isValid():
                movie.frameChanged.connect(self._on_movie_frame)
                movie.start()
                self.custom_movie = movie
                self._sync_timer()
                return

        self.custom_pixmap = QPixmap(str(path))
        self._refresh_custom_cache()

    def _on_movie_frame(self, _frame: int) -> None:
        if self.interaction_paused:
            return
        self._refresh_custom_cache()
        self.update()

    def _refresh_custom_cache(self) -> None:
        if self.size().isEmpty():
            return

        source = QPixmap()
        if self.custom_movie:
            source = self.custom_movie.currentPixmap()
        elif not self.custom_pixmap.isNull():
            source = self.custom_pixmap

        if source.isNull():
            self.custom_scaled = QPixmap()
            return

        # Scale only on frame changes / resizes, never during every paintEvent.
        self.custom_scaled = source.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        self._custom_cache_size = self.size()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._sync_timer()

    def hideEvent(self, event) -> None:
        super().hideEvent(event)
        self._sync_timer()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.mode == "Custom":
            self._refresh_custom_cache()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.theme_bg)
        t = 0.0 if not self.animations else time.perf_counter() - self.t0

        if self.mode == "Aurora":
            self._paint_aurora(painter, t)
        elif self.mode == "Nebula":
            self._paint_nebula(painter, t)
        elif self.mode == "Grid Waves":
            self._paint_grid(painter, t)
        elif self.mode == "Particles":
            self._paint_particles(painter, t)
        elif self.mode == "Static Gradient":
            self._paint_static_gradient(painter)
        elif self.mode == "Custom":
            self._paint_custom(painter)

    def _paint_static_gradient(self, p: QPainter) -> None:
        grad = QLinearGradient(0, 0, self.width(), self.height())
        c1 = QColor(self.accent)
        c1.setAlpha(95)
        c2 = QColor(self.secondary)
        c2.setAlpha(70)
        grad.setColorAt(0.0, c1)
        grad.setColorAt(0.52, QColor(self.theme_bg))
        grad.setColorAt(1.0, c2)
        p.fillRect(self.rect(), grad)

    def _paint_aurora(self, p: QPainter, t: float) -> None:
        self._paint_static_gradient(p)
        w, h = self.width(), self.height()
        blobs = [
            (0.22 + 0.10 * math.sin(t * 0.38), 0.25 + 0.12 * math.cos(t * 0.29), self.accent),
            (0.72 + 0.13 * math.cos(t * 0.31), 0.32 + 0.11 * math.sin(t * 0.35), self.secondary),
            (0.48 + 0.18 * math.sin(t * 0.22 + 1.2), 0.75 + 0.08 * math.cos(t * 0.41), self._shift_hue(self.accent, 245)),
        ]
        for nx, ny, color in blobs:
            radius = max(w, h) * 0.48
            grad = QRadialGradient(nx * w, ny * h, radius)
            c0 = QColor(color)
            c0.setAlpha(100)
            c1 = QColor(color)
            c1.setAlpha(0)
            grad.setColorAt(0.0, c0)
            grad.setColorAt(1.0, c1)
            p.fillRect(self.rect(), grad)

        p.setRenderHint(QPainter.Antialiasing, False)
        pen = QPen(QColor(255, 255, 255, 16), 1.0)
        p.setPen(pen)
        for row in range(5):
            base = h * (0.2 + row * 0.13)
            last = None
            for x in range(-20, w + 40, 30):
                y = base + math.sin(x * 0.012 + t * 0.8 + row) * (20 + row * 6)
                if last is not None:
                    p.drawLine(round(last[0]), round(last[1]), round(x), round(y))
                last = (x, y)

    def _paint_nebula(self, p: QPainter, t: float) -> None:
        w, h = self.width(), self.height()
        for nx, ny, color, speed in [
            (0.28, 0.42, self.accent, 0.10),
            (0.68, 0.55, self.secondary, -0.08),
        ]:
            x = (nx + 0.08 * math.sin(t * speed * 4)) * w
            y = (ny + 0.07 * math.cos(t * speed * 5)) * h
            grad = QRadialGradient(x, y, max(w, h) * 0.5)
            c = QColor(color)
            c.setAlpha(85)
            grad.setColorAt(0, c)
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            p.fillRect(self.rect(), grad)

        p.setRenderHint(QPainter.Antialiasing, True)
        for sx, sy, size, phase in self.stars:
            pulse = 0.55 + 0.45 * math.sin(t * 1.8 + phase * math.tau)
            c = QColor(255, 255, 255, round(50 + 115 * pulse))
            p.setPen(Qt.NoPen)
            p.setBrush(c)
            p.drawEllipse(round(sx * w), round(sy * h), max(1, round(size)), max(1, round(size)))

    def _paint_grid(self, p: QPainter, t: float) -> None:
        w, h = self.width(), self.height()
        c = QColor(self.accent)
        c.setAlpha(58)
        p.setPen(QPen(c, 1.0))
        spacing = max(40, round(min(w, h) * 0.06))
        offset = (t * 35) % spacing
        for x in range(-spacing, w + spacing, spacing):
            xx = x + offset
            p.drawLine(round(xx), 0, round(xx + math.sin(t + x * 0.01) * 30), h)
        for y in range(-spacing, h + spacing, spacing):
            yy = y + offset
            p.drawLine(0, round(yy), w, round(yy + math.cos(t + y * 0.01) * 20))
        glow = QRadialGradient(w * 0.5, h * 0.55, max(w, h) * 0.6)
        gc = QColor(self.secondary)
        gc.setAlpha(55)
        glow.setColorAt(0, gc)
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        p.fillRect(self.rect(), glow)

    def _paint_particles(self, p: QPainter, t: float) -> None:
        w, h = self.width(), self.height()
        p.setRenderHint(QPainter.Antialiasing, True)
        for x0, y0, speed, size in self.particles:
            y = (y0 + t * speed * 0.12) % 1.1 - 0.05
            x = (x0 + 0.04 * math.sin(t * speed * 4 + y0 * 9)) % 1.0
            c = QColor(self.accent if size > 2.2 else self.secondary)
            c.setAlpha(90 if size > 2.2 else 55)
            p.setPen(Qt.NoPen)
            p.setBrush(c)
            p.drawEllipse(round(x * w), round(y * h), round(size), round(size))

    def _paint_custom(self, p: QPainter) -> None:
        if self.custom_scaled.isNull():
            self._paint_aurora(p, 0.0)
            return
        x = (self.width() - self.custom_scaled.width()) // 2
        y = (self.height() - self.custom_scaled.height()) // 2
        p.drawPixmap(x, y, self.custom_scaled)
        p.fillRect(self.rect(), QColor(0, 0, 0, 75))
