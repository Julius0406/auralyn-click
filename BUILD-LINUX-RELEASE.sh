#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
exec "$ROOT/packaging/linux/build-linux.sh"
