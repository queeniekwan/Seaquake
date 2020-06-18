from websocket import create_connection
import json
import sqlite3
import time 

ws = create_connection('wss://api-pub.bitfinex.com/ws/2')

ws.send(json.dumps({"event": "subscribe", "channel": "ticker", "symbol": "tBTCUSD"}))

while True:
    timestamp = float(time.time() * 1000)
    msg = ws.recv()
    msg = json.loads(msg)
    print(msg)

    # write ticker into sqlite3 db
    if type(msg) == list:
        if not msg[1] == 'hb': 
            conn = sqlite3.connect('live ticker/ticker.db')
            c = conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS bitfinex (
                        time real,
                        price real,
                        best_bid real,
                        bid_size real,
                        best_ask real,
                        ask_size real,
                        daily_volume real
                        )""")
            

            c.execute("INSERT into bitfinex (time, price, best_bid, bid_size, best_ask, ask_size, daily_volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (timestamp, msg[1][6], msg[1][0], msg[1][1], msg[1][2], msg[1][3], msg[1][7]))
            
            conn.commit()
            conn.close()
            # print('saved to db')


ws.close()