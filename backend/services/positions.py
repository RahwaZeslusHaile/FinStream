from fastapi import HTTPException

from domain.broker import BrokerName
from mappers.positions import map_to_position
from repositories.position import (
    get_position_item,
    query_positions_by_broker,
    scan_all_positions,
)
from schemas.positions import Position


def get_all_positions_service() -> list[Position]:
    positions_data = scan_all_positions()
    if not positions_data:
        raise HTTPException(
            status_code=404,
            detail="No positions found.",
        )
    return [map_to_position(item) for item in positions_data]


def get_positions_by_broker_service(broker: BrokerName) -> list[Position]:
    positions_data = query_positions_by_broker(broker)
    if not positions_data:
        raise HTTPException(
            status_code=404,
            detail=f"No positions found for broker '{broker}'.",
        )
    return [map_to_position(item) for item in positions_data]


def get_position_service(broker: BrokerName, ticker: str) -> Position:
    item = get_position_item(broker, ticker)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=(f"Position for broker '{broker}' and ticker '{ticker}' not found."),
        )
    return map_to_position(item)
