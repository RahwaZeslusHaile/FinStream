from schemas.positions import Position


class InvalidPositionDataError(Exception):
    pass


def map_to_position(item: dict) -> Position:
    try:
        return Position(
            broker=item["broker"],
            ticker=item["ticker"],
            quantity=item["quantity"],
            market_value=item["market_value"],
        )
    except KeyError as e:
        raise InvalidPositionDataError(f"Database item is corrupt: missing field {e}")
