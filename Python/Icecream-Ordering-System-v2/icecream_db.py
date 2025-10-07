# icecream_db.py
# Small SQLite helper for the IceCream project.
import sqlite3
from typing import List, Tuple
from datetime import datetime

DB_NAME = "icecream.db"
TABLE_NAME = "orders"

def initialize_db() -> None:
    """
    Create the database and the orders table if they don't exist.
    Schema: one row per ice cream order.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number INTEGER,
            customer_name TEXT,
            flavor TEXT,
            scoops INTEGER,
            deluxe INTEGER,
            toppings TEXT,
            total REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_order(order_number: int, customer_name: str, flavor: str, scoops: int,
               deluxe: bool, toppings: List[str], total: float, created_at=None) -> None:
    """
    Insert one ice cream order into the orders table.
    toppings: list of strings (stored as comma-separated)
    deluxe: bool (stored as 0/1)
    """
    toppings_str = ", ".join(toppings) if toppings else ""
    if not created_at:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {TABLE_NAME}
            (order_number, customer_name, flavor, scoops, deluxe, toppings, total, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_number, customer_name, flavor, scoops, 1 if deluxe else 0, toppings_str, float(total), created_at))
    conn.commit()
    conn.close()

def get_all_orders() -> List[Tuple]:
    """Return all rows from orders for testing."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT id, customer_name, flavor, scoops, deluxe, toppings, total, created_at FROM {TABLE_NAME} ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_next_order_number():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(order_number) FROM orders")
    result = cursor.fetchone()[0]
    conn.close()
    return 1 if result is None else result + 1

if __name__ == "__main__":
    initialize_db()
    print(f"Initialized DB '{DB_NAME}' with table '{TABLE_NAME}'.")