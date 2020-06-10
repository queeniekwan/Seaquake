import sqlite3

# conn = sqlite3.connect('live ticker/ticker.db')
conn = sqlite3.connect('binance_daily_volume.db')
c = conn.cursor()

c.execute("SELECT * FROM binance_volume")
rows = c.fetchall()
for row in rows:
        print(row)

# conn.commit()
conn.close()
