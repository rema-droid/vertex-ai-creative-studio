#!/bin/bash
PORT=${PORT:-8080}
uv run mesop --port $PORT main.py
