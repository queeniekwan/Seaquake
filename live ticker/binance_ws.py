import time
from datetime import datetime
from binance.client import Client
from binance.websockets import BinanceSocketManager
from configparser import ConfigParser
import sqlite3

# get Config
config = ConfigParser()
config.read('config.ini')
api_key = config.get('binance', 'BINANCE_KEY')
api_secret = config.get('binance', 'BINANCE_SECRET')

# Instantiate a client
client = Client(api_key, api_secret)

# Instantiate a BinanceSocketManager, passing in the client that you instantiated
bm = BinanceSocketManager(client)


# This is our callback function
def handle_message(msg):
    if msg['e'] == 'error':
        print(msg['m'])

    elif msg['e'] == '24hrTicker':
        print(msg)
        
        # write ticker into sqlite3 db
        conn = sqlite3.connect('live ticker/ticker.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS binance (
                        time real,
                        price_change real,
                        price_change_percent real,
                        wavg real,
                        close real,
                        open real,
                        high real,
                        low real,
                        base_volume real,
                        quote_volume real
                        )""")

        c.execute("INSERT into binance (time, price_change, price_change_percent, wavg, close, open, high, low, base_volume, quote_volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (float(msg['E']), float(msg['p']), float(msg['P']), float(msg['w']), float(msg['c']), float(msg['o']), float(msg['h']), float(msg['l']), float(msg['v']), float(msg['q'])))
        
        conn.commit()
        conn.close()
        # print('saved to db')

# Start trade socket with 'BTCUSDT' and use handle_message to.. handle the message.
conn_key = bm.start_symbol_ticker_socket('BTCUSDT', handle_message)
# then start the socket manager
bm.start()

# let some data flow..
# time.sleep(10)


# stop the socket manager
# bm.stop_socket(conn_key)
