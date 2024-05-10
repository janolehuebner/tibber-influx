# -*- coding: utf-8 -*-
import os
import sys

import tibber.const
import asyncio
import aiohttp
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
#logging
logger = logging.getLogger("TibberInflux")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
#fh = logging.FileHandler('log.log')
ch.setFormatter(formatter)
#fh.setFormatter(formatter)
logger.addHandler(ch)
#logger.addHandler(fh)

logger.setLevel(logging.INFO)

__version__ = "v0.1.8"
logger.info(__version__)
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def _incoming(pkg):
    data = pkg.get("data")
    p = Pulse(data).get_datapoint()
    write_api.write(record=p, bucket=BUCKET)
    logger.info(p)


async def run():
    conn = aiohttp.TCPConnector(limit_per_host=3)
    async with aiohttp.ClientSession(trust_env=True, connector=conn) as session:
        tibber_connection = tibber.Tibber(TIBBERTOKEN, user_agent="python", websession=session)
        await tibber_connection.update_info()
    home = tibber_connection.get_homes()[0]
    await home.rt_subscribe(_incoming)

    while True:
        await asyncio.sleep(2)


loop = asyncio.new_event_loop()
loop.run_until_complete(run())
