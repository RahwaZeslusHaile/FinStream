from fastapi import HTTPException

from schemas.positions import Position


def map_to_position(item: dict) -> Position:
    try:
        return Position(
            broker=item["broker"],
            ticker=item["ticker"],
            quantity=item["quantity"],
            market_value=item["market_value"],
        )
    except KeyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid position data: missing key {e}",
        )
