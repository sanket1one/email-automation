#!/bin/bash

# Function to check if a port is in use.
check_port() {
  PORT=$1
  if lsof -i :"$PORT" >/dev/null 2>&1; then
    return 0  # Port is in use.
  else
    return 1  # Port is free.
  fi
}

Start Redis if not already running.
if check_port 6379; then
  echo "Redis is already running on port 6379. Skipping Redis startup."
else
  echo "Starting Redis..."
  osascript -e 'tell application "Terminal" to do script "redis-server"'
fi

# Start FastAPI backend in the current shell if not already running.
if check_port 8000; then
  echo "Backend is already running on port 8000. Skipping backend startup."
else
  echo "Starting FastAPI backend in the current shell..."
  source .venv/bin/activate
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  deactivate
fi
