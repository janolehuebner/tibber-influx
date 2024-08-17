

async def periodic_task():
    while True:
        try:
            # Fetch price info and write to InfluxDB
            p = Price(home.current_subscription.price_info.current).get_datapoint()
            write_api.write(record=p, bucket=BUCKET)
            logger.info(vars(p))
        except Exception as e:
            logger.exception("Error in periodic_task():")
        # Wait for the next run (e.g., every 60 seconds)
        await asyncio.sleep(3)


import asyncio
import os
import signal
import sys

import tibber
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from DataPoints import Pulse
import logging

TOKEN = os.getenv('TOKEN', '')
TIBBERTOKEN = os.getenv('TIBBERTOKEN', '')
URL = os.getenv('URL', "")
BUCKET = os.getenv('BUCKET', "tibber")
ORG = os.getenv('ORG', "Default")

# Logging configuration
logger = logging.getLogger("TibberInflux")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

__version__ = "v0.3.4"
logger.info(__version__)
loop = asyncio.get_event_loop()

logger.info("connecting to db...")
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
logger.info("connecting to tibber...")
account = tibber.Account(TIBBERTOKEN)
home = account.homes[0]
logger.info("starting subscription...")

def _incoming(data):
    try:
        p = Pulse(data).get_datapoint()
        write_api.write(record=p, bucket=BUCKET)
        logger.info(p)
    except Exception as e:
        logger.exception("Error in _incoming():")
        raise e

def timeout_handler(signum, frame):
    raise TypeError("Timeout occurred")

@home.event("live_measurement")
async def show_current_power(data):
    signal.alarm(8)
    _incoming(data)

def stop(home):
    return False

try:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(15)
    home.start_live_feed(user_agent="pulse.py/0.3.4",exit_condition=stop(home),retries=2,retry_interval=3.0)
    periodic_task_task = loop.create_task(periodic_task())

    # Wait for both tasks to complete
except TypeError:
    logger.exception("Timeout occurred while executing start_live_feed()")
    client.close()
    exit(1)
except Exception:
    logger.exception("Error in start_live_feed()")
    client.close()
    exit(41)








