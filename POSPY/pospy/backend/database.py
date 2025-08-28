"""SQLite helpers for storing POS metadata."""

import os
import sqlite3
from typing import List, Tuple

from .. import config


class Database:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or config.SQLITE_DB
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                image TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pos_order (
                id INTEGER PRIMARY KEY,
                reference TEXT,
                total REAL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def insert_product(self, name: str, price: float, image: str | None = None) -> int:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO product(name, price, image) VALUES(?, ?, ?)", (name, price, image))
        self.conn.commit()
        return cur.lastrowid

    def list_products(self) -> List[Tuple[int, str, float, str | None]]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, price, image FROM product")
        return cur.fetchall()

    def insert_order(self, reference: str, total: float) -> int:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO pos_order(reference, total) VALUES(?, ?)", (reference, total))
        self.conn.commit()
        return cur.lastrowid

    def close(self) -> None:
        self.conn.close()


def main() -> None:
    db = Database()
    print("Database initialised at", db.db_path)


if __name__ == "__main__":
    main()
