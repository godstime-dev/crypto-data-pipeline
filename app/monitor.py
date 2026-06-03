import logging
import requests
from app.config import LOG_FILE, LOG_LEVEL, DISCORD_WEBHOOK_URL

def send_discord_alert(message: str):
    """
    Sends alert message to Discord via webhook.
    Fails gracefully without breaking pipeline execution.
    """

    if not DISCORD_WEBHOOK_URL:
        return

    payload = {"content": message}

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            timeout=5
            )
        response.raise_for_status()

    except Exception as e:
        logging.warning(f"Discord alert failed: {e}")


# SETUP

logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )

logging.getLogger("apscheduler").setLevel(logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, LOG_LEVEL))

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logging.getLogger().addHandler(console_handler)


def log_info(message: str):
    logging.info(message, stacklevel=2)


def log_error(message: str):
    logging.error(message, stacklevel=2)