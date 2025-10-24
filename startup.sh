#!/bin/sh
python wait_db.py
alembic -c app/alembic.ini upgrade head
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
