from kraken_wsclient_py import kraken_wsclient_py as client
import sqlite3

def my_handler(message):
    print(message)

    # write ticker into sqlite3 db
    if type(message) == list:
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
                    (message[1][0], message[1][1], message[1][2], message[1][3], message[1][4], message[1][5], message[1][6], message[1][7], message[1][8]))
        
        conn.commit()
        conn.close()
        # print('saved to db')


my_client = client.WssClient()
my_client.start()

my_client.subscribe_public(
    subscription = {
        'name': 'ohlc'
    },
    pair = ['BTC/USD'],
    callback = my_handler
)
