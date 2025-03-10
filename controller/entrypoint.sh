#!/bin/sh

if [ -n "$CONTROLLER_PORT_FIRST" ]; then
  PORT=$CONTROLLER_PORT_FIRST
  echo "Using CONTROLLER_PORT_FIRST environment variable for port: $PORT"
elif [ -n "$CONTROLLER_PORT_SECOND" ]; then
  PORT=$CONTROLLER_PORT_SECOND
  echo "Using CONTROLLER_PORT_SECOND environment variable for port: $PORT"
else
  PORT="UNDEFINED"
  echo "No environment variable set, using default port: $PORT"
fi

trap 'kill -TERM $PID' TERM INT

poetry run uvicorn src.controller.main:app --host 0.0.0.0 --port "${PORT}" --reload &

PID=$!
wait $PID
