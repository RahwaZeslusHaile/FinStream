def get_broker_a_data():
    return {
        "source": "Broker_A",
        "positions": [
            {"symbol": "AAPL", "qty": 100, "price": 150.25},
            {"symbol": "TSLA", "qty": -50, "price": 200.50},
        ],
    }


def get_broker_b_data():
    return [
        {"ticker": "MSFT", "amount": 200, "market_value": 310.00},
        {"ticker": "AMZN", "amount": 150, "market_value": 135.50},
    ]
