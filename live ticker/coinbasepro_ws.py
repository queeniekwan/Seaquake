import asyncio
from copra.websocket import Channel, Client
from datetime import datetime 
import sqlite3

class Ticker(Client):
    def on_message(self, msg):
        if msg['type'] == 'error':
            print(msg)

        elif msg['type'] == 'ticker':
            print(msg)

            UTC = datetime.strptime(msg['time'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000

            # write ticker into sqlite3 db 
            conn = sqlite3.connect('live ticker/ticker.db')
            c = conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS coinbasepro (
                            time real,
                            price real,
                            best_bid real,
                            best_ask real,
                            last_size real,
                            taker_side text
                            )""")

            c.execute("INSERT into coinbasepro (time, price, best_bid, best_ask, last_size, taker_side) VALUES (?, ?, ?, ?, ?, ?)",
                        (UTC, msg['price'], msg['best_bid'], msg['best_ask'], msg['last_size'], msg['side']))
            
            conn.commit()
            conn.close()
            print('saved to db')

loop = asyncio.get_event_loop()
channel = Channel('ticker', 'BTC-USD')
ws = Ticker(loop, channel)

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(ws.close())
    loop.close()