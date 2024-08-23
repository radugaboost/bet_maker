#!/usr/bin/env bash

echo "Start service"

alembic upgrade head

exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT