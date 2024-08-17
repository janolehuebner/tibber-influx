#!/bin/bash

# Print environment variables to a file
printenv > /app/env

# Start the cron service
service cron start

# Run your main application script (pulse.py) in the background
python3 /app/pulse.py &

# Run the other script periodically in the background
(
  while true; do
    python3 /app/get_price.py >> /var/log/other_script.log 2>&1
    sleep 3  # Sleep for 60 seconds (1 minute)
  done
) &

# Keep the container running and output both cron logs and pulse.py output
tail -f /var/log/cron.log &
wait -n
