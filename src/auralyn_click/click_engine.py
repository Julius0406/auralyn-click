from __future__ import annotations

import math
import random
import threading
import time
from dataclasses import dataclass

from PySide6.QtCore import QThread, Signal
from pynput import mouse


@dataclass(slots=True)
class ClickConfig:
    interval: float
    button: str
    click_type: str
    repeat_mode: str
    repeat_count: int
    position_mode: str
    pos_x: int
    pos_y: int
    random_delay: bool
    random_delay_ms: int
    random_position: bool
    random_position_radius: int
    press_duration_ms: int
    start_delay_ms: int
    burst_enabled: bool
    burst_count: int
    burst_pause_ms: int
    time_limit_enabled: bool
    time_limit_seconds: int


class ClickWorker(QThread):
    count_changed = Signal(int)
    state_text = Signal(str)
    errored = Signal(str)
    done = Signal()

    def __init__(self, config: ClickConfig):
        super().__init__()
        self.config = config
        self.stop_event = threading.Event()
        self.total_clicks = 0

    def stop(self) -> None:
        self.stop_event.set()

    def _interruptible_wait(self, seconds: float) -> bool:
        return self.stop_event.wait(max(0.0, seconds))

    def run(self) -> None:
        try:
            if self.config.start_delay_ms > 0:
                remaining = self.config.start_delay_ms / 1000.0
                while remaining > 0 and not self.stop_event.is_set():
                    self.state_text.emit(f"Start in {remaining:.1f}s")
                    chunk = min(0.1, remaining)
                    if self._interruptible_wait(chunk):
                        break
                    remaining -= chunk
                if self.stop_event.is_set():
                    return

            controller = mouse.Controller()
            button = {
                "left": mouse.Button.left,
                "right": mouse.Button.right,
                "middle": mouse.Button.middle,
            }[self.config.button]

            clicks_per_action = {"single": 1, "double": 2, "triple": 3}.get(self.config.click_type, 1)
            max_actions = self.config.repeat_count if self.config.repeat_mode == "count" else None
            action_count = 0
            burst_actions = 0
            started_at = time.perf_counter()
            deadline = started_at

            while not self.stop_event.is_set():
                if self.config.time_limit_enabled:
                    if time.perf_counter() - started_at >= self.config.time_limit_seconds:
                        break

                if self.config.position_mode == "fixed":
                    x = self.config.pos_x
                    y = self.config.pos_y
                    if self.config.random_position and self.config.random_position_radius > 0:
                        radius = self.config.random_position_radius
                        angle = random.random() * math.tau
                        distance = radius * math.sqrt(random.random())
                        x += round(math.cos(angle) * distance)
                        y += round(math.sin(angle) * distance)
                    controller.position = (x, y)

                for _ in range(clicks_per_action):
                    if self.stop_event.is_set():
                        break
                    if self.config.press_duration_ms > 0:
                        controller.press(button)
                        if self._interruptible_wait(self.config.press_duration_ms / 1000.0):
                            controller.release(button)
                            break
                        controller.release(button)
                    else:
                        controller.click(button, 1)
                    self.total_clicks += 1

                action_count += 1
                burst_actions += 1

                if self.total_clicks % 4 == 0 or self.config.interval >= 0.01:
                    self.count_changed.emit(self.total_clicks)

                if max_actions is not None and action_count >= max_actions:
                    break

                if self.config.burst_enabled and burst_actions >= self.config.burst_count:
                    burst_actions = 0
                    self.state_text.emit("Burst-Pause")
                    if self._interruptible_wait(self.config.burst_pause_ms / 1000.0):
                        break
                    deadline = time.perf_counter()

                jitter = 0.0
                if self.config.random_delay and self.config.random_delay_ms > 0:
                    jitter = random.uniform(
                        -self.config.random_delay_ms / 1000.0,
                        self.config.random_delay_ms / 1000.0,
                    )

                step = max(0.001, self.config.interval + jitter)
                deadline += step
                now = time.perf_counter()
                if deadline < now - step:
                    deadline = now + step

                if self._interruptible_wait(deadline - time.perf_counter()):
                    break

            self.count_changed.emit(self.total_clicks)
        except Exception as exc:
            self.errored.emit(str(exc))
        finally:
            self.done.emit()
