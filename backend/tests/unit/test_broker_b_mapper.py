from decimal import Decimal

import pytest

from domain.broker import BrokerName
from mappers.broker_b import normalize_broker_b


def test_normalize_broker_b_success():
    raw_data = [
        {"ticker": "MSFT", "amount": 200, "market_value": 310.00},
        {"ticker": "AMZN", "amount": 150, "market_value": 135.50},
    ]
    positions = normalize_broker_b(raw_data)

    assert len(positions) == 2
    assert positions[0].ticker == "MSFT"
    assert positions[0].quantity == Decimal("200")
    assert positions[0].market_value == Decimal("310.00")
    assert positions[0].broker == BrokerName.broker_b


def test_normalize_broker_b_skips_invalid_items():
    raw_data = [
        {"ticker": "MSFT", "amount": 200, "market_value": 310.00},
        {"ticker": "GOOG", "amount": None, "market_value": 100.0},
        {"ticker": "NFLX", "amount": "invalid", "market_value": 50},
        {"amount": 100, "market_value": 50.0},
        "corrupted_string_item",
    ]
    positions = normalize_broker_b(raw_data)

    assert len(positions) == 1
    assert positions[0].ticker == "MSFT"


def test_normalize_broker_b_invalid_data_type():
    with pytest.raises(
        TypeError,
        match="Input data for Broker B must be a list.",
    ):
        normalize_broker_b({"not": "a_list"})
