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
weekday = False
hour = False

if timeframe == '1d':
    weekday = True
if timeframe == '1h':
    hour = True

if weekday:
    new_path = f'ohlvc/seasonality/weekday/{exchange_id}_weekday.csv'
if hour:
    new_path = f'ohlvc/seasonality/daily_hour/{exchange_id}_daily_hour.csv'

# Get, clean, and store data
scrape_candles_to_csv(raw_path, exchange_id, max_retries, symbol, timeframe, since, limit)
formatdata(raw_path, new_path, headers, isodate, weekday, hour)