import asyncio
import os
import signal
import sys
import logging

import tibber
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from DataPoints import Pulse, Price

TOKEN = os.getenv('TOKEN', '')
TIBBERTOKEN = os.getenv('TIBBERTOKEN', '')
URL = os.getenv('URL', "")
BUCKET = os.getenv('BUCKET', "tibber")
ORG = os.getenv('ORG', "Default")

# Logging configuration
logger = logging.getLogger("TibberInflux")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

__version__ = "v0.4.0"
logger.info(__version__)

# Initialize InfluxDB client
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# Initialize Tibber account
account = tibber.Account(TIBBERTOKEN)
home = account.homes[0]


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


async def show_current_power(data):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(8)
    _incoming(data)


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


async def main():
    loop = asyncio.get_event_loop()
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(15)

    try:
        # Start the live feed in a separate task
        home_feed_task = loop.create_task(home.start_live_feed(
            user_agent="pulse.py/0.4.0",
            exit_condition=lambda: False,
            retries=2,
            retry_interval=3.0,
            callback=show_current_power
        ))

        # Start the periodic task
        periodic_task_task = loop.create_task(periodic_task())

        # Wait for both tasks to complete
        await asyncio.gather(home_feed_task, periodic_task_task)

    except TypeError:
        logger.exception("Timeout occurred while executing start_live_feed()")
        client.close()
        sys.exit(1)
    except Exception:
        logger.exception("Error in start_live_feed()")
        client.close()
        sys.exit(41)


if __name__ == "__main__":
    asyncio.run(main())
