from datetime import datetime, timezone
from app.monitor import log_error


def transform_crypto_data(api_response):
    """
    Transforms nested API response into a flat database-ready structure.
    """

    transformed_data = []
    skipped = 0

    for coin_name, price_data in api_response.items():

        usd_price = price_data.get("usd")

        if usd_price is None:
            log_error(f"Skipping {coin_name}: missing USD price")
            skipped += 1
            continue

        transformed_record = {
            "coin": coin_name,
            "price_usd": usd_price,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        transformed_data.append(transformed_record)

    return transformed_data
