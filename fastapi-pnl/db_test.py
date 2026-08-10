import sqlite3

conn = sqlite3.connect("pnl.db")

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, coin TEXT, action TEXT, amount REAL, price REAL)")

cursor.execute(
    "INSERT INTO transactions (coin, action, amount, price) VALUES (?, ?, ?, ?)", 
    ("bitcoin", "buy", 0.5, 64000)
)

cursor.execute(
    "INSERT INTO transactions (coin, action, amount, price) VALUES (?, ?, ?, ?)", 
    ("ethereum", "buy", 1, 3000)
)

cursor.execute(
    "INSERT INTO transactions (coin, action, amount, price) VALUES (?, ?, ?, ?)", 
    ("solana", "sell", 10, 200)
)

cursor.execute("SELECT * FROM transactions")

conn.commit()

rows = cursor.fetchall()
print(rows)

conn.close()