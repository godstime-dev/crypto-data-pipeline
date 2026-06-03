from datetime import datetime, timezone
from app.collector import fetch_crypto_prices
from app.validator import validate_price_data
from app.transformer import transform_crypto_data
from app.trends import get_market_signal
from app.database import (
    insert_price,
    get_latest_price,
    get_last_alert_time,
    update_alert_state,
    get_recent_prices
    )
from app.monitor import log_info, log_error, send_discord_alert
from app.config import (PRICE_CHANGE_THRESHOLD_PERCENT, ALERT_COOLDOWN_SECONDS)


def run_pipeline():
    log_info("Pipeline execution started")

    try:
        # EXTRACT
        api_response = fetch_crypto_prices()

        # VALIDATE
        validate_price_data(api_response)

        # TRANSFORM
        records = transform_crypto_data(api_response)

        now = datetime.now(timezone.utc)

        for record in records:
            coin = record["coin"]
            new_price = record["price_usd"]
            timestamp = record["timestamp"]

            last_price = get_latest_price(coin)

            if last_price is None:
                insert_price(coin, new_price, timestamp)
                log_info(f"Inserted {coin} ${new_price:,.2f}")
                continue

            # SAFETY CHECK
            if last_price <= 0:
                continue

            # PRICE CHANGE
            change_percent = ((new_price - last_price) / last_price) * 100
            
            direction = "SPIKE" if change_percent > 0 else "CRASH"
            sign = "+" if change_percent > 0 else ""

            # TREND ANALYSIS
            recent_prices = get_recent_prices(coin, limit=5)
            signal = get_market_signal(recent_prices)

            trend = signal["trend"]
            volatility = signal["volatility"]
            momentum = signal["momentum"]

            log_info(
                f"{coin} | Trend: {trend} | "
                f"Volatility: {volatility:.6f} | "
                f"Momentum: {momentum:.2f}"
                )

            # ALERT COOLDOWN
            last_time_raw = get_last_alert_time(coin)

            last_time = (
                datetime.fromisoformat(last_time_raw)
                if last_time_raw else None)

            cooldown_passed = (
                last_time is None or
                (now - last_time).total_seconds() >= ALERT_COOLDOWN_SECONDS)

            # ALERT CONDITION
            if abs(change_percent) >= PRICE_CHANGE_THRESHOLD_PERCENT and cooldown_passed:

                alert_msg = (
                    f" ALERT \n"
                    f"{coin.upper()} moved {sign}{change_percent:.2f}%\n"
                    f"Trend: {trend}\n"
                    f"Price: ${last_price:,.2f} → ${new_price:,.2f}")

                log_info(f"Alert triggered for {coin}: {sign}{change_percent:.2f}%")
                send_discord_alert(alert_msg)

                update_alert_state(coin, now.isoformat())


            insert_price(coin, new_price, timestamp)

            log_info(f"Inserted {coin} ${new_price:,.2f}")

        log_info("Pipeline cycle completed successfully")

    except Exception as e:
        log_error(f"Pipeline failed: {e}")