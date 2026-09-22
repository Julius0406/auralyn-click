from __future__ import annotations

import fcntl
import os
import socket
import tempfile
import threading
import time
from pathlib import Path

from PySide6.QtCore import QObject, Signal

UID = os.getuid()
SOCKET_PATH = Path(tempfile.gettempdir()) / f"auralyn-click-{UID}.sock"
LOCK_PATH = Path(tempfile.gettempdir()) / f"auralyn-click-{UID}.lock"


def acquire_single_instance():
    fd = LOCK_PATH.open("a+")
    try:
        fcntl.flock(fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        fd.seek(0)
        fd.truncate()
        fd.write(str(os.getpid()))
        fd.flush()
        return fd
    except BlockingIOError:
        fd.close()
        return None


def send_command(command: str, retries: int = 1, delay: float = 0.08) -> bool:
    for _ in range(max(1, retries)):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(0.4)
            sock.connect(str(SOCKET_PATH))
            sock.sendall(command.encode("utf-8"))
            try:
                sock.recv(16)
            except Exception:
                pass
            sock.close()
            return True
        except Exception:
            time.sleep(delay)
    return False


class IPCBridge(QObject):
    command = Signal(str)


class IPCServer(threading.Thread):
    def __init__(self, bridge: IPCBridge):
        super().__init__(daemon=True)
        self.bridge = bridge
        self._running = True
        self._socket: socket.socket | None = None

    def run(self) -> None:
        try:
            if SOCKET_PATH.exists():
                SOCKET_PATH.unlink()
        except OSError:
            pass

        try:
            self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._socket.bind(str(SOCKET_PATH))
            os.chmod(SOCKET_PATH, 0o600)
            self._socket.listen(8)
            self._socket.settimeout(0.5)
        except Exception as exc:
            print("Auralyn Click IPC failed:", exc)
            return

        while self._running:
            try:
                conn, _ = self._socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            try:
                command = conn.recv(128).decode("utf-8", errors="ignore").strip().lower()
                if command:
                    self.bridge.command.emit(command)
                conn.sendall(b"ok")
            except Exception:
                pass
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

    def stop(self) -> None:
        self._running = False
        try:
            if self._socket:
                self._socket.close()
        except Exception:
            pass
