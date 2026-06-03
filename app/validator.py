class ValidationError(Exception):
    pass

def validate_price_data(data):
    """
    Validates API response structure for crypto prices.
    """
    required_coins = ["bitcoin", "ethereum"]

    for coin in required_coins:

        if coin not in data:
            raise ValidationError(f"Missing coin: {coin}")

        if "usd" not in data[coin]:
            raise ValidationError(f"Missing USD value for {coin}")

        if not isinstance(data[coin]["usd"], (int, float)):
            raise ValidationError(f"{coin} price must be numeric")