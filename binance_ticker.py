import urllib.request
import json
from pprint import pprint
from datetime import datetime
import sqlite3

# 
def get_json(url):
    ''' Given a properly formatted URL for a JSON web API request, 
    return a Python JSON object containing the response to that request.
    '''
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data

# futures
BASE_URL_F = 'https://fapi.binance.com/fapi/v1/ticker/24hr'
futures_tickers = get_json(BASE_URL_F)

futures_volume = 0
for ticker in futures_tickers:
    # print(ticker['symbol'], ticker['weightedAvgPrice'], ticker['volume'], float(ticker['weightedAvgPrice'])*float(ticker['volume']))
    futures_volume += float(ticker['volume'])*float(ticker['weightedAvgPrice'])

# spot
BASE_URL = 'https://api.binance.com/api/v3/ticker/24hr'
spot_tickers = get_json(BASE_URL)
spot_volume = 0
for ticker in spot_tickers:
    # print(ticker['symbol'], ticker['weightedAvgPrice'], ticker['volume'], float(ticker['weightedAvgPrice'])*float(ticker['volume']))
    spot_volume += float(ticker['volume'])*float(ticker['weightedAvgPrice'])

# print and save to sql database
time = datetime.now()
print(f'Time:{time} \nBinance 24hr Volume:{spot_volume:.0f} \nBinance 24hr Derivatives Volume:{futures_volume:.0f}')

conn = sqlite3.connect('binance_daily_volume.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS binance_volume (Time text, TotalVolume real, DerivativesVolume real)""")
c.execute("""INSERT INTO binance_volume(Time, TotalVolume, DerivativesVolume) VALUES (?,?,?)""", (str(time), spot_volume, futures_volume))

conn.commit()
conn.close()
