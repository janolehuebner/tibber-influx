#!/bin/bash

sleep 2

python3 /get_price.py >> /var/log/cron.log 2>&1