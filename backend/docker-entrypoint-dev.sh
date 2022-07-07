#! /usr/bin/env bash

alembic upgrade head

python ./app/backend_start.py



uvicorn app.api.server:app --reload --workers 1 --host 0.0.0.0 --port 8000