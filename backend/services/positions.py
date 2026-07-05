from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

from domain.broker import BrokerName
from integrations.dynamodb import table
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


def get_all_positions_service() -> list[Position]:
    scan_params = {}
    positions = []
    while True:
        response = table.scan(**scan_params)
        for item in response.get("Items", []):
            positions.append(map_to_position(item))

        if "LastEvaluatedKey" not in response:
            break
        scan_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]

    return positions


def get_positions_by_broker_service(broker: BrokerName) -> list[Position]:
    response = table.query(KeyConditionExpression=Key("broker").eq(broker))
    items = response.get("Items", [])
    mapped_positions = [map_to_position(item) for item in items]
    if not mapped_positions:
        raise HTTPException(
            status_code=404,
            detail=f"No positions found for broker '{broker}'.",
        )
    return mapped_positions


def get_position_service(broker: BrokerName, ticker: str) -> Position:
    response = table.get_item(Key={"broker": broker, "ticker": ticker})
    item = response.get("Item")
    if not item:
        raise HTTPException(
            status_code=404,
            detail=(f"Position for broker '{broker}' and ticker '{ticker}' not found."),
        )
    return map_to_position(item)
