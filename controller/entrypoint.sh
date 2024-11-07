#!/bin/sh


trap 'kill -TERM $PID' TERM INT
poetry run flask --app src.controller.main run --host=0.0.0.0 --port=5000 &

PID=$!
wait $PID
