import sqlite3

conn = sqlite3.connect('live ticker/ticker.db')
c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS binance (
#                 UTC int PRIMARY KEY,
#                 time text,
#                 symbol text,
#                 price_change real,
#                 price_change_percent real,
#                 weighted_average_price real,
#                 close_price real,
#                 open_price real,
#                 high_price real,
#                 low_price real,
#                 total_traded_base_asset_volume real,
#                 total_traded_quote_asset_volume real
#                 )""")

# c.execute("""INSERT INTO binance VALUES (1590536285832, '2020-05-26 19:29:57', 'BTCUSDT', -84.56, -0.949, 8859.3564936, 8828.51, 8913.07, 9017.67, 8700.0, 58386.321019, 517265232.25730544)""")

c.execute("SELECT * FROM binance")
rows = c.fetchall()
for row in rows:
        print(row)

# conn.commit()
# print(c.lastrowid)
conn.close()
