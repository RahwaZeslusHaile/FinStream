from decimal import Decimal

from domain.broker import BrokerName
from schemas.positions import Position


def normalize_broker_a(data: dict) -> list[Position]:
    positions = []
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary")
    if "positions" not in data:
        raise ValueError("Missing 'positions' key in input data")
    if not isinstance(data["positions"], list):
        raise TypeError("'positions' must be a list")
    for item in data.get("positions", []):
        qty = Decimal(str(item["qty"]))
        price = Decimal(str(item["price"]))
        positions.append(
            Position(
                broker=BrokerName.broker_a,
                ticker=item["symbol"],
                quantity=qty,
                market_value=qty * price,
            )
        )
    return positions
