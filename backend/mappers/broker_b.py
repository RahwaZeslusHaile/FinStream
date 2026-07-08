from decimal import Decimal

from domain.broker import BrokerName
from schemas.positions import Position


def normalize_broker_b(data: dict) -> list[Position]:
    positions = []
    for item in data:
        qty = Decimal(str(item["amount"]))
        mv = Decimal(str(item["market_value"]))
        positions.append(
            Position(
                broker=BrokerName.broker_b,
                ticker=item["ticker"],
                quantity=qty,
                market_value=mv,
            )
        )
    return positions
