from __future__ import annotations

import getpass
import os
import socket
import tempfile
import threading
import time
import zlib
from pathlib import Path

from PySide6.QtCore import QObject, Signal

APP_ID = "auralyn-click"
USER_KEY = getpass.getuser().encode("utf-8", errors="ignore")
IPC_HOST = "127.0.0.1"
IPC_PORT = 43100 + (zlib.crc32(USER_KEY) % 1000)
LOCK_PATH = Path(tempfile.gettempdir()) / f"{APP_ID}-{zlib.crc32(USER_KEY):08x}.lock"


def acquire_single_instance():
    """Acquire an OS-backed lock and keep the returned file open for app lifetime."""
    if os.name == "nt":
        import msvcrt
        fd = open(LOCK_PATH, "a+b")
        fd.seek(0, os.SEEK_END)
        if fd.tell() == 0:
            fd.write(b"0")
            fd.flush()
        fd.seek(0)
        try:
            msvcrt.locking(fd.fileno(), msvcrt.LK_NBLCK, 1)
            return fd
        except OSError:
            fd.close()
            return None

    import fcntl
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


def release_single_instance(fd) -> None:
    if fd is None:
        return
    try:
        if os.name == "nt":
            import msvcrt
            fd.seek(0)
            msvcrt.locking(fd.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(fd.fileno(), fcntl.LOCK_UN)
    except Exception:
        pass
    try:
        fd.close()
    except Exception:
        pass


def send_command(command: str, retries: int = 1, delay: float = 0.08) -> bool:
    for _ in range(max(1, retries)):
        try:
            sock = socket.create_connection((IPC_HOST, IPC_PORT), timeout=0.4)
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
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((IPC_HOST, IPC_PORT))
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
