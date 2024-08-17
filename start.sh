#!/bin/bash

python3 /app/pulse.py &

# Run the other script at 0, 15, 30, 45, and 60 minutes
(
  while true; do
    current_minute=$(date +'%M')
    if [[ "$current_minute" == "00" || "$current_minute" == "15" || "$current_minute" == "30" || "$current_minute" == "45" || "$current_minute" == "00" ]]; then
      python3 /app/get_price.py
    fi
    sleep 60  # Check every minute
  done
) &

wait -n
