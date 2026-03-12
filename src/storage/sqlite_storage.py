import sqlite3
import json
from typing import List

from src.models.transaction import Transaction


class SQLiteStorage:

    def __init__(self):
        self.conn = sqlite3.connect("registry.db", check_same_thread=False)
        self.create_table()

    def create_table(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            hash TEXT PRIMARY KEY,
            data TEXT,
            tx_json TEXT
        )
        """)

        self.conn.commit()

    def add_transaction(self, tx: Transaction):

        tx_json = json.dumps(tx.dict(), default=str)

        self.conn.execute(
            "INSERT INTO transactions VALUES (?, ?, ?)",
            (tx.Hash, tx.Data, tx_json)
        )

        self.conn.commit()

    def get_transactions(self) -> List[Transaction]:

        rows = self.conn.execute(
            "SELECT tx_json FROM transactions"
        ).fetchall()

        return [
            Transaction.parse_raw(row[0])
            for row in rows
        ]

    def get_last_transaction(self):

        row = self.conn.execute(
            "SELECT tx_json FROM transactions ORDER BY rowid DESC LIMIT 1"
        ).fetchone()

        if not row:
            return None

        return Transaction.parse_raw(row[0])


storage = SQLiteStorage()
