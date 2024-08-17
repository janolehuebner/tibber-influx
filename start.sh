#!/bin/bash

# Start the cron service
service cron start

# Run your main application script (pulse.py) in the background
python3 /pulse.py &

# Keep the container running and output both cron logs and pulse.py output
tail -f /var/log/cron.log &
wait -n
