import os
import requests
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from DataPoints import Price


TOKEN=os.getenv('TOKEN', '')
TIBBERTOKEN=os.getenv('TIBBERTOKEN', '')
URL = os.getenv('URL',"" )
BUCKET = os.getenv('BUCKET',"tibber" )
ORG = os.getenv('ORG',"Default" )

# URL of the Tibber API
url = 'https://api.tibber.com/v1-beta/gql'

# Request headers
headers = {
    'authority': 'api.tibber.com',
    'accept': 'application/json',
    'authorization': f'Bearer {TIBBERTOKEN}',
    'content-type': 'application/json',
    'user-agent': 'python 3.10',
}

# GraphQL query
query = '{"query":"{ viewer { homes { currentSubscription { priceInfo { current { total } } } } } }"}'



client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
# Make the HTTP POST request
response = requests.post(url, headers=headers, data=query)

# Check for successful response
if response.status_code == 200:
    # Print the response content (JSON data)
    print(response.json())
else:
    print(f'Error: HTTP {response.status_code}')

p = Price(response.json()).get_datapoint()
write_api.write(record=p, bucket=BUCKET)
