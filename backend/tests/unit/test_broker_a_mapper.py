from decimal import Decimal

import pytest

from domain.broker import BrokerName
from mappers.broker_a import normalize_broker_a


def test_normalize_broker_a_success():
    """Test that valid Broker A data normalizes into Position schemas."""
    raw_data = {
        "source": "Broker_A",
        "positions": [
            {"symbol": "AAPL", "qty": 100, "price": 150.25},
            {"symbol": "TSLA", "qty": -50, "price": 200.50},
        ],
    }
    positions = normalize_broker_a(raw_data)

    assert len(positions) == 2
    assert positions[0].ticker == "AAPL"
    assert positions[0].quantity == Decimal("100")
    assert positions[0].market_value == Decimal("15025.00")
    assert positions[0].broker == BrokerName.broker_a


def test_normalize_broker_a_skips_invalid_and_missing_items():
    """Test that missing fields or corrupt numbers are skipped gracefully."""
    raw_data = {
        "source": "Broker_A",
        "positions": [
            {"symbol": "AAPL", "qty": 100, "price": 150.25},
            {"symbol": "MSFT", "qty": None, "price": 300.00},
            {"symbol": "GOOG", "qty": "invalid", "price": 100.00},
            {"symbol": "AMZN", "qty": 50},
            "corrupted_row_string",
        ],
    }
    positions = normalize_broker_a(raw_data)

    assert len(positions) == 1
    assert positions[0].ticker == "AAPL"


def test_normalize_broker_a_invalid_data_type():
    with pytest.raises(TypeError):
        normalize_broker_a("not_a_dictionary")

    with pytest.raises(ValueError):
        normalize_broker_a({"source": "Broker_A"})
