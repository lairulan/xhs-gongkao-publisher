#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$ROOT_DIR"

echo "[1/5] Checking Bash syntax"
bash -n scripts/check.sh

echo "[2/5] Checking Python syntax"
"$PYTHON_BIN" -m py_compile scripts/batch-screenshot.py

echo "[3/5] Checking CLI help"
"$PYTHON_BIN" scripts/batch-screenshot.py --help >/dev/null

echo "[4/5] Checking Python dependencies"
"$PYTHON_BIN" - <<'PY'
import importlib.util
import sys

required = ("playwright",)
missing = [name for name in required if importlib.util.find_spec(name) is None]

if missing:
    print("[error] Missing Python package(s):", ", ".join(missing))
    print("[hint] Run: python3 -m pip install -r requirements.txt")
    sys.exit(1)

print("[ok] Python dependencies available")
PY

echo "[5/5] Checking required repository files"
test -f README.md
test -f SKILL.md
test -f STATUS.md
test -f references/publish-sop.md

echo "[done] Repository checks passed"
