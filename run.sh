#!/bin/bash

set -e

exec uvicorn src.api:app --host 0.0.0.0 --port 80 --loop uvloop &
exec python3 -m src.bot