import statistics

def calculate_trend_signal(prices):
    """
    Simple directional bias based on net movement.
    """

    if len(prices) < 2:
        return "INSUFFICIENT_DATA"

    net_change = prices[-1] - prices[0]

    if net_change > 0:
        return "UPTREND"
    elif net_change < 0:
        return "DOWNTREND"
    else:
        return "SIDEWAYS"


def calculate_volatility(prices):
    """
    Measures price instability using standard deviation of returns.
    """
    if len(prices) < 2:
        return 0.0
    returns = [
        (prices[i] - prices[i - 1]) / prices[i - 1]
        for i in range(1, len(prices))
    ]
    return statistics.pstdev(returns)


def calculate_momentum(prices):
    """
    Normalized directional movement over the window.
    """
    if len(prices) < 2:
        return 0.0
    return (prices[-1] - prices[0]) / prices[0]


def get_market_signal(prices):
    """
    Unified market signal object used by pipeline.
    """
    return {
        "trend": calculate_trend_signal(prices),
        "volatility": calculate_volatility(prices),
        "momentum": calculate_momentum(prices)
    }