import asyncio
from copra.websocket import Channel, Client
from datetime import datetime 
import sqlite3

class Ticker(Client):
    def on_message(self, msg):
        if msg['type'] == 'error':
            print(msg)
        else:
            if msg['type'] == 'ticker':
                print(msg)

                UTC = datetime.strptime(msg['time'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000  
                # Connect to sqlite database
                conn = sqlite3.connect('live ticker/ticker.db')
                c = conn.cursor()

                c.execute("""CREATE TABLE IF NOT EXISTS coinbasepro (
                                UTC int PRIMARY KEY,
                                time text,
                                symbol text,
                                price real,
                                best_bid real,
                                best_ask real,
                                last_size real
                                )""")

                c.execute("INSERT or IGNORE into coinbasepro (UTC, time, symbol, price, best_bid, best_ask, last_size) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (UTC, msg['time'], msg['product_id'], msg['price'], msg['best_bid'], msg['best_ask'], msg['last_size'])
                            )
                
                conn.commit()
                conn.close()
                print(f'ticker saved to database, time: {UTC}')

loop = asyncio.get_event_loop()
channel = Channel('ticker', 'BTC-USD')
ws = Ticker(loop, channel)

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(ws.close())
    loop.close()