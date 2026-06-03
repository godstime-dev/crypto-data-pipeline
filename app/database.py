from app.config import DB_NAME
import sqlite3


def create_table():
    """Initializes the price table with a composite unique constraint."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(coin, timestamp)
                )""")
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alert_state (
            coin TEXT PRIMARY KEY,
            last_alert_time TEXT
            )""")
        conn.commit()


def insert_price(coin, price, timestamp):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO prices (coin, price, timestamp)
            VALUES (?, ?, ?)
            """,
            (coin, price, timestamp))
        conn.commit()


def get_latest_price(coin):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT price
            FROM prices
            WHERE coin = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (coin,))

        result = cursor.fetchone()
        return result[0] if result else None
    
def update_alert_state(coin, timestamp):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alert_state (coin, last_alert_time)
            VALUES (?, ?)
            ON CONFLICT(coin)
            DO UPDATE SET last_alert_time = excluded.last_alert_time
        """, (coin, timestamp))
        conn.commit()

def get_last_alert_time(coin):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT last_alert_time
            FROM alert_state
            WHERE coin = ?
        """, (coin,))
        row = cursor.fetchone()

        return row[0] if row else None
    
def get_recent_prices(coin, limit=5):
    """
    Returns most recent prices for trend detection.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT price
            FROM prices
            WHERE coin = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (coin, limit))

        rows = cursor.fetchall()

    return [row[0] for row in rows][::-1]