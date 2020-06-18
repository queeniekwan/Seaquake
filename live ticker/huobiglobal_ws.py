from websocket import create_connection
import gzip
import json
import sqlite3

ws = create_connection('wss://api-aws.huobi.pro/ws')

ws.send(json.dumps({"sub": "market.btcusdt.kline.1min", "id": "01"}))

while True:
    msg = ws.recv()
    msg = gzip.decompress(msg)
    msg = json.loads(msg)
    print(msg)

    # response to ping messages to remain active
    if 'ping' in msg:
        id = msg['ping']
        ws.send(json.dumps({"pong": id}))
    
    # write ticker into sqlite3 db
    if 'tick' in msg:
        conn = sqlite3.connect('live ticker/ticker.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS huobiglobal (
                    time real,
                    open real,
                    close real,
                    low real,
                    high real,
                    amount real,
                    volume real,
                    count int
                    )""")
        

        c.execute("INSERT into huobiglobal (time, open, close, low, high, amount, volume, count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (msg['ts'], msg['tick']['open'], msg['tick']['close'], msg['tick']['low'], msg['tick']['high'], msg['tick']['amount'], msg['tick']['vol'], msg['tick']['count']))
        
        conn.commit()
        conn.close()
        # print('saved to db')

ws.close()

