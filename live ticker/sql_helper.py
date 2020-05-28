import sqlite3

conn = sqlite3.connect('live ticker/ticker.db')
c = conn.cursor()

c.execute("SELECT * FROM coinbasepro")
rows = c.fetchall()
for row in rows:
        print(row)

# conn.commit()
conn.close()
