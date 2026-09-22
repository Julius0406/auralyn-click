from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class SegmentControl(QWidget):
    changed = Signal(str)

    def __init__(self, items: list[tuple[str, str]], value: str, parent=None):
        super().__init__(parent)
        self.items = items
        self.current = value
        self.animations = True
        self.setObjectName("segmentWrap")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)

        self.indicator = QFrame(self)
        self.indicator.setObjectName("segmentIndicator")
        self.indicator.lower()
        self.buttons: list[tuple[QPushButton, str]] = []

        for text, val in items:
            button = QPushButton(text)
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setProperty("segment", True)
            button.clicked.connect(lambda _checked=False, v=val: self.set_value(v, True))
            layout.addWidget(button, 1)
            self.buttons.append((button, val))

        self.set_value(value, False)

    def value(self) -> str:
        return self.current

    def set_value(self, value: str, emit: bool = False) -> None:
        self.current = value
        for button, val in self.buttons:
            button.setChecked(val == value)
        self._move_indicator(self.animations and self.isVisible())
        if emit:
            self.changed.emit(value)

    def _target_rect(self) -> QRect:
        for button, val in self.buttons:
            if val == self.current:
                g = button.geometry()
                return QRect(g.x() + 3, g.y() + 3, max(0, g.width() - 6), max(0, g.height() - 6))
        return QRect()

    def showEvent(self, event):
        super().showEvent(event)
        self.indicator.setGeometry(self._target_rect())
        self.indicator.show()
        self.indicator.lower()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._move_indicator(False)

    def _move_indicator(self, animate: bool) -> None:
        target = self._target_rect()
        if not target.isValid():
            return
        if not animate:
            self.indicator.setGeometry(target)
            return
        self._anim = QPropertyAnimation(self.indicator, b"geometry", self)
        self._anim.setDuration(190)
        self._anim.setStartValue(self.indicator.geometry())
        self._anim.setEndValue(target)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.start()


class Card(QFrame):
    def __init__(self, title: str, subtitle: str | None = None, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 16, 18, 18)
        outer.setSpacing(11)
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        outer.addWidget(title_label)
        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("muted")
            sub.setWordWrap(True)
            outer.addWidget(sub)
        self.content = QVBoxLayout()
        self.content.setSpacing(10)
        outer.addLayout(self.content)

import math
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QBrush, QFont, QPainter, QPen


class LiveOrb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 150)
        self.phase = 0.0
        self.running = False
        self.animations = True
        self.accent = QColor("#7C5CFF")
        self.timer = QTimer(self)
        self.timer.setInterval(16)  # 60 Hz is smoother under load than repainting at ~166 Hz
        self.interaction_paused = False
        self.timer.timeout.connect(self._tick)

    def set_state(self, running: bool, animations: bool, accent: str) -> None:
        self.running = running
        self.animations = animations
        self.accent = QColor(accent)
        if running and animations and not self.interaction_paused:
            self.timer.start()
        else:
            self.timer.stop()
        self.update()

    def set_interaction_paused(self, paused: bool) -> None:
        self.interaction_paused = paused
        if self.running and self.animations and not paused:
            self.timer.start()
        else:
            self.timer.stop()
        self.update()

    def _tick(self) -> None:
        self.phase = (self.phase + 0.026) % 1.0
        self.update()

    def paintEvent(self, event) -> None:
        side = min(self.width(), self.height())
        cx, cy = self.width() / 2, self.height() / 2
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if self.running:
            for i in range(4):
                t = (self.phase + i / 4) % 1.0
                radius = side * (0.20 + 0.32 * t)
                color = QColor(self.accent)
                color.setAlpha(round(115 * (1.0 - t)))
                p.setPen(QPen(color, max(2.0, side * 0.015)))
                p.setBrush(Qt.NoBrush)
                p.drawEllipse(
                    round(cx - radius), round(cy - radius),
                    round(radius * 2), round(radius * 2)
                )

        core = side * (0.225 + (0.012 * math.sin(self.phase * math.tau) if self.running else 0.0))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self.accent if self.running else QColor("#4B5364")))
        p.drawEllipse(round(cx-core), round(cy-core), round(core*2), round(core*2))

        p.setPen(QColor("white"))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(max(14, round(side * 0.11)))
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, "ON" if self.running else "OFF")
