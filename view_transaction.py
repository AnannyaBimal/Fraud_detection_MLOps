import sqlite3
import pandas as pd

from database import DB_PATH

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY timestamp DESC",
        conn
    )
    
    query = """SELECT COUNT(*) AS total_transactions FROM transactions
    WHERE amount > 30000"""
    df = pd.read_sql_query(query, conn)
    print(df)
    
print(df.head(10))