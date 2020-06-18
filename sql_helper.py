import sqlite3

conn = sqlite3.connect('live ticker/ticker.db')
# conn = sqlite3.connect('binance_daily_volume.db')
c = conn.cursor()

# c.execute("SELECT * FROM binance_volume")
# c.execute("SELECT * FROM binance")
# c.execute("SELECT * FROM coinbasepro")
# rows = c.fetchall()
# for row in rows:
#         print(row)

c.execute("DROP TABLE kraken")

# conn.commit()
conn.close()
