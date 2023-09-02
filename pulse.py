# -*- coding: utf-8 -*-
import os
import random

import tibber.const
import asyncio
import aiohttp
import tibber
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from DataPoints import Pulse

TOKEN=os.getenv('TOKEN', '')
TIBBERTOKEN=os.getenv('TIBBERTOKEN', '')
URL = os.getenv('URL',"" )
BUCKET = os.getenv('BUCKET',"tibber" )
ORG = os.getenv('ORG',"Default" )

__version__ = "v0.0.2"
print(f"tibber_{__version__}")

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def _incoming(pkg):
    try:
        data = pkg.get("data")
        if data is None:
            exit(1)
        p = Pulse(data).get_datapoint()
        write_api.write(record=p, bucket=BUCKET)
        print(p)
        return True
    except:
        exit(1)

async def run():
    async with aiohttp.ClientSession() as session:
        if session.closed:
            print("session closed")
            exit(1)
        tibber_connection = tibber.Tibber(TIBBERTOKEN, websession=session, user_agent="python")
        await tibber_connection.update_info()
    home = tibber_connection.get_homes()[0]
    try:
         await home.rt_subscribe(_incoming)

    except:
        exit(1)

    while 1:
        await asyncio.sleep(5)



loop = asyncio.get_event_loop()
loop.run_until_complete(run())
