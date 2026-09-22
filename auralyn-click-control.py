#!/usr/bin/env python3
from __future__ import annotations

import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

UID = os.getuid()
SOCKET_PATH = Path(tempfile.gettempdir()) / f"auralyn-click-{UID}.sock"
COMMAND = (sys.argv[1] if len(sys.argv) > 1 else "toggle").strip().lower()
VALID = {"toggle", "start", "stop", "capture", "show"}

if COMMAND not in VALID:
    sys.exit(2)


def send(command: str) -> bool:
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
        return False


if send(COMMAND):
    sys.exit(0)

# The hard-stop must never launch the app.
if COMMAND in {"stop", "capture"}:
    sys.exit(0)

launcher = Path.home() / ".local" / "bin" / "auralyn-click"
try:
    subprocess.Popen([str(launcher)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
except Exception:
    sys.exit(1)

for _ in range(35):
    time.sleep(0.1)
    if send(COMMAND):
        sys.exit(0)

sys.exit(1)
