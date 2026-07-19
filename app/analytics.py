from statistics import mean
from app.database import (
    get_latest_market_snapshots,
    get_recent_prices,
    )


def get_movers(threshold=2.0):
    """
    Returns coins whose 24h change exceeds the threshold.
    """

    snapshot = get_latest_market_snapshots()

    movers = []

    for coin in snapshot:
        change = coin["change_24h"]

        if change is None:
            continue

        if abs(change) >= threshold:
            movers.append({
                "coin": coin["coin"],
                "price": coin["price_usd"],
                "change_24h": round(change, 2),
                "direction": "UP" if change > 0 else "DOWN"
            })

    movers.sort(
        key=lambda x: abs(x["change_24h"]),
        reverse=True
    )

    return movers


def get_volume_surge():
    """
    Ranks coins by current 24h trading volume.
    """

    snapshot = get_latest_market_snapshots()

    ranked = sorted(
        snapshot,
        key=lambda x: x["volume_24h"] or 0,
        reverse=True
    )

    return [
        {
            "coin": row["coin"],
            "volume_24h": row["volume_24h"]
        }
        for row in ranked
    ]


def get_trend_strength(coin):
    """
    Determines whether price momentum is strengthening.
    """

    prices = get_recent_prices(coin, limit=5)

    if len(prices) < 5:
        return {
            "coin": coin,
            "trend": "INSUFFICIENT_DATA"
        }

    increases = 0
    decreases = 0

    for previous, current in zip(prices[:-1], prices[1:]):
        if current > previous:
            increases += 1
        elif current < previous:
            decreases += 1

    momentum = prices[-1] - prices[0]

    if increases == 4:
        trend = "STRONG_UPTREND"

    elif decreases == 4:
        trend = "STRONG_DOWNTREND"

    elif momentum > 0:
        trend = "WEAK_UPTREND"

    elif momentum < 0:
        trend = "WEAK_DOWNTREND"

    else:
        trend = "SIDEWAYS"

    return {
        "coin": coin,
        "trend": trend,
        "momentum": round(momentum, 4)
    }


def get_market_sentiment():
    """
    Returns an overall market sentiment signal.
    """

    snapshot = get_latest_market_snapshots()

    changes = [
        coin["change_24h"]
        for coin in snapshot
        if coin["change_24h"] is not None
    ]

    bullish = sum(change > 0 for change in changes)
    bearish = sum(change < 0 for change in changes)

    average_change = mean(changes) if changes else 0

    if bullish >= 4:
        sentiment = "STRONGLY_BULLISH"

    elif bearish >= 4:
        sentiment = "STRONGLY_BEARISH"

    elif bullish > bearish:
        sentiment = "BULLISH"

    elif bearish > bullish:
        sentiment = "BEARISH"

    else:
        sentiment = "MIXED"

    return {
        "sentiment": sentiment,
        "bullish_coins": bullish,
        "bearish_coins": bearish,
        "average_change_24h": round(average_change, 2)
    }


def get_correlation_signal():
    """
    Simple market correlation signal.
    Determines whether coins are moving together.
    """

    snapshot = get_latest_market_snapshots()

    changes = [
        coin["change_24h"]
        for coin in snapshot
        if coin["change_24h"] is not None
    ]

    bullish = sum(change > 0 for change in changes)
    bearish = sum(change < 0 for change in changes)

    if bullish == len(changes) or bearish == len(changes):
        signal = "HIGH_CORRELATION"

    elif bullish >= 4 or bearish >= 4:
        signal = "MODERATE_CORRELATION"

    else:
        signal = "LOW_CORRELATION"

    return {
        "signal": signal,
        "bullish": bullish,
        "bearish": bearish
    }