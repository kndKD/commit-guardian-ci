#!/bin/sh
# Run the Flask app locally (port 5000 by default, PORT to override).
# Usage: ./scripts/run.sh
set -e
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi
PORT="${PORT:-5000}" .venv/bin/python -m app.main
