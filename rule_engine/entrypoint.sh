#!/bin/sh

trap 'kill -TERM $PID' TERM INT

poetry run rule_engine &

PID=$!
wait $PID
