import sqlite3

conn = sqlite3.connect('live ticker/ticker.db')
# conn = sqlite3.connect('binance_daily_volume.db')
c = conn.cursor()

# c.execute("SELECT * FROM binance_volume")

# c.execute("SELECT * FROM binance")
# c.execute("SELECT * FROM coinbasepro")
# c.execute("SELECT * FROM bitfinex")
c.execute("SELECT * FROM huobiglobal")

rows = c.fetchall()
for row in rows:
        print(row)

# c.execute("DROP TABLE huobiglobal")

# conn.commit()
conn.close()
