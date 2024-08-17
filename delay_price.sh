#!/bin/bash
source /app/env
printenv
sleep 2

python3 /app/get_price.py >> /var/log/cron.log 2>&1