import sqlite3
from database import DB_PATH

with sqlite3.connect(DB_PATH) as conn:

    conn.execute("DROP TABLE IF EXISTS transaction_features")

print("Old transaction_features table removed.")
