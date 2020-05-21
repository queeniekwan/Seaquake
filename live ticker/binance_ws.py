import time
from datetime import datetime
from binance.client import Client
from binance.websockets import BinanceSocketManager
from configparser import ConfigParser

# get Config
config = ConfigParser()
config.read('live ticker/config.ini')
api_key = config.get('binance', 'BINANCE_KEY')
api_secret = config.get('binance', 'BINANCE_SECRET')

# Instantiate a client
client = Client(api_key, api_secret)

# Instantiate a BinanceSocketManager, passing in the client that you instantiated
bm = BinanceSocketManager(client)

# This is our callback function. For now, it just prints messages as they come.
def handle_message(msg):
    if msg['e'] == 'error':
        print(msg['m'])

    else:
        timestamp = msg['E'] / 1000
        timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        log = {'Time': timestamp, 
                'Symbol': msg['s'], 
                'Price change': msg['p'], 
                'Price change percent': msg['P'],
                'Weighted average price': msg['w'],
                'Close price': msg['c'],
                'Open price': msg['o'],
                'High price': msg['h'],
                'Low price': msg['l'],
                'Total traded base asset volume': msg['v'],
                'Total traded quote asset volume': msg['q'],
        }
        print(log)

# Start trade socket with 'ETHBTC' and use handle_message to.. handle the message.
conn_key = bm.start_symbol_ticker_socket('BTCUSDT', handle_message)
# then start the socket manager
bm.start()

# let some data flow..
time.sleep(10)


# stop the socket manager
bm.stop_socket(conn_key)
