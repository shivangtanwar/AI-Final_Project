#!/usr/bin/env bash
set -e
PYTHON=${PYTHON:-python3}
if ! command -v "$PYTHON" >/dev/null; then
  echo "python3 not found"; exit 1;
fi
if ! "$PYTHON" -m pip --version >/dev/null 2>&1; then
  echo "pip missing"; exit 1;
fi
"$PYTHON" -m pip install --user --break-system-packages -r backend/requirements.txt || true
exec "$PYTHON" -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000