import asyncio
import os
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

__version__ = "v0.3.0"
logger.info(__version__)

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def _incoming(data):
    try:
        p = Pulse(data).get_datapoint()
        write_api.write(record=p, bucket=BUCKET)
        logger.info(p)
    except Exception as e:
        logger.exception("Error in _incoming():")
        raise e

account = tibber.Account(TIBBERTOKEN)
home = account.homes[0]

@home.event("live_measurement")
async def show_current_power(data):
    _incoming(data)

home.start_live_feed(user_agent="UserAgent/0.0.1")
logger.info("Livefeed started")
while home.live_feed.running:
    event = home.event("live_measurement")
