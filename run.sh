#!/bin/bash

set -e

exec uvicorn api.main:app --host 0.0.0.0 --port 80 --workers 8 --loop uvloop &
exec python3 -m bot.main