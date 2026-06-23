from app.config import DB_NAME
import duckdb


def create_table():
    """Initializes the prices and alert_state tables."""
    with duckdb.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS market_data(
            coin TEXT NOT NULL,
            price_usd DOUBLE NOT NULL,
            market_cap DOUBLE,
            volume_24h DOUBLE,
            change_24h DOUBLE,
            timestamp TIMESTAMPTZ NOT NULL,
            UNIQUE(coin, timestamp))
            """
            )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alert_state (
            coin TEXT PRIMARY KEY,
            last_alert_time TIMESTAMPTZ)
            """
            )


def insert_market_data(data: dict):
    """Inserts a dictionary containing all transformed market metrics."""
    with duckdb.connect(DB_NAME) as conn:
        conn.execute(
            """
            INSERT INTO market_data (coin, price_usd, market_cap, volume_24h, change_24h, timestamp)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (coin, timestamp) DO NOTHING
            """,
            (
                data["coin"],
                data["price_usd"],
                data["market_cap"],
                data["volume_24h"],
                data["change_24h"],
                data["timestamp"]
                )
                )


def get_latest_price(coin):
    with duckdb.connect(DB_NAME) as conn:
        result = conn.execute("""
            SELECT price_usd
            FROM market_data
            WHERE coin = $1
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (coin,)
            ).fetchone()
        
        return result[0] if result else None
    

def update_alert_state(coin, timestamp):
    with duckdb.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO alert_state (coin, last_alert_time)
            VALUES ($1, $2)
            ON CONFLICT(coin)
            DO UPDATE SET last_alert_time = excluded.last_alert_time""", 
            (coin, timestamp))


def get_last_alert_time(coin):
    with duckdb.connect(DB_NAME) as conn:
        row = conn.execute(
            """
            SELECT last_alert_time
            FROM alert_state
            WHERE coin = $1
            """,
            (coin,)).fetchone()

        return row[0] if row else None
    

def get_recent_prices(coin, limit=5):
    """
    Returns most recent prices for trend detection.
    """
    with duckdb.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT price_usd
            FROM market_data
            WHERE coin = $1
            ORDER BY timestamp DESC
            LIMIT $2""", 
            (coin, limit)
        ).fetchall()

    return [row[0] for row in rows][::-1]