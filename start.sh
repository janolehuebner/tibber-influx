#!/bin/bash

python3 /app/pulse.py &

# Run the other script periodically in the background
(
  while true; do
    python3 /app/get_price.py >> /var/log/other_script.log 2>&1
    sleep 3  # Sleep for 60 seconds (1 minute)
  done
) &


wait -n
