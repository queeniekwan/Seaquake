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


# This is our callback function. For now, it just prints messages as they come.
def handle_message(msg):
    if msg['e'] == 'error':
        print(msg['m'])

    else:
        timestamp = msg['E'] / 1000
        timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        log = {'UTC': int(msg['E']),
                'Time': timestamp, 
                'Symbol': msg['s'], 
                'Price change': float(msg['p']), 
                'Price change percent': float(msg['P']),
                'Weighted average price': float(msg['w']),
                'Close price': float(msg['c']),
                'Open price': float(msg['o']),
                'High price': float(msg['h']),
                'Low price': float(msg['l']),
                'Total traded base asset volume': float(msg['v']),
                'Total traded quote asset volume': float(msg['q']),
        }
        print(log)

        # Connect to sqlite3 database
        conn = sqlite3.connect('live ticker/ticker.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS binance (
                        UTC int PRIMARY KEY,
                        time text,
                        symbol text,
                        price_change real,
                        price_change_percent real,
                        weighted_average_price real,
                        close_price real,
                        open_price real,
                        high_price real,
                        low_price real,
                        total_traded_base_asset_volume real,
                        total_traded_quote_asset_volume real
                        )""")

        c.execute("INSERT into binance (UTC, time, symbol, price_change, price_change_percent, weighted_average_price, close_price, open_price, high_price, low_price, total_traded_base_asset_volume, total_traded_quote_asset_volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (log['UTC'], log['Time'], log['Symbol'], log['Price change'], log['Price change percent'],
                    log['Weighted average price'], log['Close price'], log['Open price'], log['High price'], log['Low price'],
                    log['Total traded base asset volume'], log['Total traded quote asset volume'])
                    )
        
        conn.commit()
        conn.close()

# Start trade socket with 'BTCUSDT' and use handle_message to.. handle the message.
conn_key = bm.start_symbol_ticker_socket('BTCUSDT', handle_message)
# then start the socket manager
bm.start()

# let some data flow..
# time.sleep(10)


# stop the socket manager
# bm.stop_socket(conn_key)
