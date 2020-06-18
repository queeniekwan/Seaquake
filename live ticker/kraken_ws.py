from kraken_wsclient_py import kraken_wsclient_py as client
import sqlite3

def my_handler(msg):
    print(msg)

    if type(msg) == dict:
        if msg['event'] == 'error':
            try:
                connect_ws()
            except:
                print(msg)

    # write ticker into sqlite3 db
    if type(msg) == list:
        conn = sqlite3.connect('live ticker/ticker.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS kraken (
                    time real, 
                    etime real,
                    open real,
                    high real,
                    low real,
                    close real,
                    vwap real,
                    volume real,
                    count real
                    )""")

        c.execute("INSERT INTO kraken (time, etime, open, high, low, close, vwap, volume, count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (msg[1][0], msg[1][1], msg[1][2], msg[1][3], msg[1][4], msg[1][5], msg[1][6], msg[1][7], msg[1][8]))
        
        conn.commit()
        conn.close()
        # print('saved to db')

def connect_ws():
    my_client = client.WssClient()
    my_client.start()

    my_client.subscribe_public(
        subscription = {
            'name': 'ohlc'
        },
        pair = ['BTC/USD'],
        callback = my_handler
    )

def main():
    connect_ws()

if __name__ == "__main__":
    main()
