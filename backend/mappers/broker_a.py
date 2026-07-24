import logging
from decimal import Decimal, InvalidOperation

from domain.broker import BrokerName, normalize_broker_name
from schemas.positions import Position

logger = logging.getLogger(__name__)


def normalize_broker_a(data: dict) -> list[Position]:
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary")

    source = data.get("source")

    if normalize_broker_name(source) != BrokerName.broker_a:
        raise ValueError(
            f"Invalid broker source: expected {BrokerName.broker_a.value}, got {source}"
        )

    positions_data = data.get("positions")

    if positions_data is None:
        raise ValueError("'positions' is missing from input data")

    if not isinstance(positions_data, list):
        raise ValueError("'positions' must be a list")

    positions = []

    for item in positions_data:
        if not isinstance(item, dict):
            logger.warning("Skipping invalid position item: %s", item)
            continue

        ticker = item.get("symbol")
        qty_raw = item.get("qty")
        price_raw = item.get("price")

        if ticker is None or qty_raw is None or price_raw is None:
            logger.warning(
                "Skipping position with missing required fields: %s",
                item,
            )
            continue

        try:
            quantity = Decimal(str(qty_raw))
            price = Decimal(str(price_raw))

        except (InvalidOperation, ValueError, TypeError):
            logger.warning(
                "Skipping position with invalid numeric values: %s",
                item,
            )
            continue

        try:
            position = Position(
                broker=BrokerName.broker_a,
                ticker=ticker,
                quantity=quantity,
                market_value=quantity * price,
            )

        except ValueError:
            logger.exception(
                "Pydantic validation failed for position: %s",
                item,
            )
            continue

        positions.append(position)

    return positions
