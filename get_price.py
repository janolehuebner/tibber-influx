import os
import sys
import tibber
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from DataPoints import Price
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

__version__ = "v0.4.0"
logger.info(__version__)

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

account = tibber.Account(TIBBERTOKEN)
home = account.homes[0]
p = Price(home.current_subscription.price_info.current).get_datapoint()
write_api.write(record=p, bucket=BUCKET)
logger.info(vars(p))