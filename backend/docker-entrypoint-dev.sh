#! /usr/bin/env bash

python ./app/backend_start.py

alembic upgrade head

uvicorn app.api.server:app --reload --workers 1 --host 0.0.0.0 --port 8000