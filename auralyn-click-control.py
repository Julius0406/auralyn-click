#!/usr/bin/env python3
import os, sys
from pathlib import Path
ROOT = Path.home() / ".local" / "share" / "auralyn-click" / "src"
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
try:
    from auralyn_click.ipc import send_command
except Exception:
    sys.exit(1)
cmd = (sys.argv[1] if len(sys.argv)>1 else "toggle").strip().lower()
if cmd not in {"toggle","start","stop","capture","show"}: sys.exit(2)
sys.exit(0 if send_command(cmd) else 1)
