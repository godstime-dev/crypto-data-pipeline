import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR.parent / "data"
LOG_DIR = BASE_DIR.parent / "logs"

# DIRECTORIES
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# API CONFIG
API_URL = "https://api.coingecko.com/api/v3/simple/price"
COINS = "bitcoin,ethereum"
CURRENCY = "usd"

# PIPELINE CONFIG
SLEEP_INTERVAL_SECONDS = 300
RETRY_COUNT = 5
RETRY_BACKOFF_SECONDS = 2
ALERT_COOLDOWN_SECONDS = 300
API_MIN_INTERVAL_SECONDS = 15

DB_NAME = str(DATA_DIR / "crypto.db")
LOG_FILE = str(LOG_DIR / "pipeline.log")

LOG_LEVEL = "INFO"

PRICE_CHANGE_THRESHOLD_PERCENT = 2.0
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")