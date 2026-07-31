from collections import defaultdict
from decimal import Decimal

from schemas.positions import Position


def consolidate_positions(positions: list[Position]) -> list[Position]:

    if not positions:
        return []

    consolidated_map = defaultdict(lambda: {"quantity": Decimal("0"), "market_value": Decimal("0")})

    for pos in positions:
        key = (pos.broker, pos.ticker)
        consolidated_map[key]["quantity"] += pos.quantity
        consolidated_map[key]["market_value"] += pos.market_value

    consolidated_list = []
    for (broker, ticker), totals in consolidated_map.items():
        consolidated_list.append(
            Position(
                broker=broker,
                ticker=ticker,
                quantity=totals["quantity"],
                market_value=totals["market_value"],
            )
        )

    return consolidated_list
