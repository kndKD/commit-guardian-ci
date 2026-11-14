#!/bin/sh
# Run the test suite. Usage: ./scripts/test.sh [--cov]
# Creates .venv and installs dev requirements on first run.
set -e
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements-dev.txt
fi
if [ "$1" = "--cov" ]; then
  .venv/bin/python -m pytest -q --cov=app --cov=guardian --cov-report=term-missing
else
  .venv/bin/python -m pytest -q
fi
