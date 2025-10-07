from icecream_db import initialize_db
import sqlite3

DB_NAME = "icecream.db"

# Connect and drop the old table
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS orders")
conn.commit()
conn.close()
print("Old table dropped successfully.")

# Re-initialize
initialize_db()
print("Database re-initialized with new empty table.")