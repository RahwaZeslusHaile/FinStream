import logging
from decimal import Decimal, InvalidOperation

from domain.broker import BrokerName
from schemas.positions import Position

logger = logging.getLogger(__name__)


def normalize_broker_b(data: list) -> list[Position]:
    if not isinstance(data, list):
        raise TypeError("Input data for Broker B must be a list.")

    if not data:
        raise ValueError("Input data for Broker B is empty.")

    positions = []

    for item in data:
        if not isinstance(item, dict):
            logger.warning(
                "Skipping invalid item: %s. Expected a dictionary.",
                item,
            )
            continue

        ticker = item.get("ticker")
        amount_raw = item.get("amount")
        market_value_raw = item.get("market_value")

        if not ticker or amount_raw is None or market_value_raw is None:
            logger.warning(
                "Skipping item due to missing required field: %s",
                item,
            )
            continue

        try:
            quantity = Decimal(str(amount_raw))
            market_value = Decimal(str(market_value_raw))

        except (
            InvalidOperation,
            TypeError,
            ValueError,
        ) as exc:
            logger.warning(
                "Skipping item due to invalid numeric values: %s. Error: %s",
                item,
                exc,
            )
            continue

        positions.append(
            Position(
                broker=BrokerName.broker_b,
                ticker=ticker,
                quantity=quantity,
                market_value=market_value,
            )
        )

    return positions
