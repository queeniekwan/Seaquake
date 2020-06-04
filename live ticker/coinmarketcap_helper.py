from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = "https://pro-api.coinmarketcap.com/v1/exchange/listings/historical"
parameters = {
  'slug':'binance',
  'limit':'5',
  'convert':'USD',
  'timestamp':'2020-06-01T00:00:00.000Z'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'f286d719-5fe0-4eb2-8dfc-88e3c3901063',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)