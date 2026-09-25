#!/bin/sh
set -e

# Apply pending Alembic migrations before booting the API.
cd "$(dirname "$0")"
alembic upgrade head

exec uvicorn launchpad.main:app --host 0.0.0.0 --port 8080 --reload
