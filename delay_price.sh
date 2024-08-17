#!/bin/bash
export PYTHONPATH=/usr/local/lib/python3.12/site-packages
sleep 2

/usr/local/bin/python3 /get_price.py >> /var/log/cron.log 2>&1