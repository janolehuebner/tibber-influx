#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import time

from dateutil.parser import parse


print("tibberpulse-influxdb")
import tibber.const
import asyncio
import aiohttp
import tibber
# settings from EnvionmentValue
TOKEN=os.getenv('TOKEN', '')
TIBBERTOKEN=os.getenv('TIBBERTOKEN', '')
URL = os.getenv('URL',"" )
BUCKET = os.getenv('BUCKET',"tibber" )
ORG = os.getenv('ORG',"Default" )

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "Default"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def _callback(pkg):
    try:
        data = pkg.get("data")
        if data is None:
            return
        lm=data.get("liveMeasurement")
        print(lm)
        write_to_db(data)
        return lm
    except Exception as e:
        raise e


def write_to_db(data,bucket = BUCKET):

    measurement = data['liveMeasurement']
    timestamp = measurement['timestamp']
    power = measurement['power']
    lastMeterConsumption = measurement['lastMeterConsumption']

    tags = {"adress":""}
    fields = {
            "power": float(power),
            "lastMeterConsumption": float(lastMeterConsumption)
        }
    datapoint = {"fields": fields,
                 "tags": tags,
                 "measurement": "pulse",
                 time: timestamp

                 }
    p = Point(measurement_name="pulse").from_dict(datapoint)
    write_api.write(record=p, bucket=bucket)





async def run():
    async with aiohttp.ClientSession() as session:
        tibber_connection = tibber.Tibber(TIBBERTOKEN, websession=session, user_agent="python")
        await tibber_connection.update_info()
    home = tibber_connection.get_homes()[0]
    try:
        await home.rt_subscribe(_callback)
    except:
        raise Exception("Session gone")

    while True:
      await asyncio.sleep(4)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except:
    exit(1)