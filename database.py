
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "database.db"


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:

        # Main transactions table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                customer_id TEXT,
                amount REAL,
                merchant TEXT,
                city TEXT,
                device TEXT,
                timestamp TEXT
            )
        """)

        # Quarantine table. Keep this name in sync with ingestion.py and
        # dashboard.py, which both write/read quarantined transactions.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quarantined_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT,
                raw_data TEXT,
                rejection_reason TEXT NOT NULL,
                rejected_at TEXT NOT NULL
            )
        """)

        # Older versions of this project created the table without the "d".
        # Copy existing rows so databases created by those versions continue
        # to work with ingestion.py and the dashboard.
        legacy_table = conn.execute("""
            SELECT 1 FROM sqlite_master
            WHERE type = 'table' AND name = 'quarantine_transactions'
        """).fetchone()
        if legacy_table:
            conn.execute("""
                INSERT OR IGNORE INTO quarantined_transactions
                    (id, transaction_id, raw_data, rejection_reason, rejected_at)
                SELECT id, transaction_id, raw_data, rejection_reason, rejected_at
                FROM quarantine_transactions
            """)

        # Transaction features table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transaction_features (
                transaction_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                amount REAL NOT NULL,
                txn_count_5m INTEGER NOT NULL,
                amount_sum_1h REAL NOT NULL,
                avg_prior_amount REAL,
                amount_ratio REAL,
                city_changed INTEGER NOT NULL,
                feature_timestamp TEXT NOT NULL,
                FOREIGN KEY (transaction_id)
                REFERENCES transactions(transaction_id)
            )
        """)
        
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS fraud_predictions (
                    transaction_id TEXT PRIMARY KEY,
                    fraud_score REAL NOT NULL,
                    is_suspicious INTEGER NOT NULL,
                    model_version TEXT NOT NULL,
                    predicted_at TEXT NOT NULL,
                    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
                )
        """)

    print("Database and tables ready at:", DB_PATH)


if __name__ == "__main__":
    create_database()
