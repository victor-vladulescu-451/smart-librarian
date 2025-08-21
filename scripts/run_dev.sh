#!/usr/bin/env bash

# run it in bash chmod +x scripts/run_dev.sh
# This is a small helper to run the app in dev. 
# - it loads your .env, runs uvicorn backend.main:app --reload for hot‑reload

set -euo pipefail
export $(grep -v '^#' .env | xargs) 2>/dev/null || true
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

