#!/bin/bash

set -e

source /opt/fastapi_app/venv/bin/activate
exec uvicorn main:app --host 0.0.0.0 --port 8000