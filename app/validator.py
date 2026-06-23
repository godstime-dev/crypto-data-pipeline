from app.monitor import log_info
from app.config import COINS
class ValidationError(Exception):
    pass

def validate_price_data(data):
    """
    Validates API response structure for crypto prices.
    """
    required_coins = COINS

    for coin in required_coins:

        if coin not in data:
            raise ValidationError(f"Missing coin: {coin}")

        if "usd" not in data[coin]:
            raise ValidationError(f"Missing USD value for {coin}")

        if not isinstance(data[coin]["usd"], (int, float)):
            raise ValidationError(f"{coin} price must be numeric")
        
        for field in ["usd_market_cap", "usd_24h_vol", "usd_24h_change"]:
            if field not in data[coin]:
                log_info(f"Warning: {coin} missing {field} — will store as None")