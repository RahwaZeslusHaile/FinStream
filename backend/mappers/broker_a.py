from decimal import Decimal

from schemas.positions import Position


def normalize_broker_a(data: dict) -> list[Position]:
    positions = []
    for item in data.get("positions", []):
        qty = Decimal(str(item["qty"]))
        price = Decimal(str(item["price"]))
        positions.append(
            Position(
                broker=data.get("source", "Broker_A"),
                ticker=item["symbol"],
                quantity=qty,
                market_value=qty * price,
            )
        )
    return positions
