#!/bin/bash

python3 /app/pulse.py &

# Run the other script periodically in the background
(
  while true; do
    python3 /app/get_price.py
    sleep 900
  done
) &


wait -n
