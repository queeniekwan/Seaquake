from ohlvc_data_cleaning import formatdata
from fetch_ohlcv_csv import scrape_candles_to_csv

# OHLVC data parameters
raw_path  = 'ohlvc/crandles.csv'
exchange_id = 'binance'
max_retries = 3
symbol = 'BTC/USDT'
timeframe = '1h'
since = '2019-01-01T00:00:00Z' #iso8601 format
limit = 100 

# Data formating parameters
headers = True
isodate = True
year = True
weekday = True
hour = True

new_path = f'ohlvc/seasonality/{exchange_id}_hourly.csv'


# Get, clean, and store data
scrape_candles_to_csv(raw_path, exchange_id, max_retries, symbol, timeframe, since, limit)
formatdata(raw_path, new_path, headers, isodate, year, weekday, hour)