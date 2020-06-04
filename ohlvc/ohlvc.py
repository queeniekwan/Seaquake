from ohlvc_data_cleaning import formatdata
from fetch_ohlcv_csv import scrape_candles_to_csv

USDT_MARKETS = ['BTC/USDT']

# OHLVC data parameters
raw_path  = 'ohlvc/crandles.csv'
exchange_id = 'binance'
max_retries = 3
symbol = 'XLM/USDT'
timeframe = '1M'
since = '2020-01-01T00:00:00Z' #iso8601 format
limit = 6

# Data formating parameters
headers = True
isodate = True
year = False
weekday = False
hour = False

symbol_n = symbol.replace('/',' ')

new_path = f'ohlvc/seasonality/binance_volume/{symbol_n}.csv'


# Get, clean, and store data
scrape_candles_to_csv(raw_path, exchange_id, max_retries, symbol, timeframe, since, limit)
formatdata(raw_path, new_path, headers, isodate, year, weekday, hour)