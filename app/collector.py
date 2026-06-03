import time
import requests
from threading import Lock
from app.monitor import log_info, log_error
from app.config import (
    API_URL,
    RETRY_COUNT,
    RETRY_BACKOFF_SECONDS,
    API_MIN_INTERVAL_SECONDS
    )


_api_lock = Lock()
_last_api_call = 0


def fetch_crypto_prices():
    global _last_api_call

    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
        }

    # RATE LIMIT PROTECTION
    with _api_lock:
        now = time.time()

        if now - _last_api_call < API_MIN_INTERVAL_SECONDS:
            time.sleep(API_MIN_INTERVAL_SECONDS - (now - _last_api_call))

        _last_api_call = time.time()

    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(API_URL, params=params, timeout=10)

            if response.status_code == 429:
                wait_time = RETRY_BACKOFF_SECONDS * (2 ** attempt)
                log_info(f"Rate limited (429). Backing off {wait_time}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            wait_time = RETRY_BACKOFF_SECONDS * (2 ** attempt)
            log_error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(wait_time)

    raise Exception("API failed after all retry attempts")