from typing import Union

from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

from app import app
from etl.service import run_etl_sync_logic
from integrations.dynamodb import table
from mock.broker import get_broker_a_data, get_broker_b_data
from schemas.brokers import BrokerAResponse, BrokerBPosition
from schemas.etl import EtlSyncResponse
from schemas.positions import Position
from services.positions import map_to_position


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/mock/broker-a", response_model=BrokerAResponse)
def get_broker_a():
    return get_broker_a_data()


@app.get("/mock/broker-b", response_model=list[BrokerBPosition])
def get_broker_b():
    return get_broker_b_data()


@app.get(
    "/mock/{broker_name}",
    response_model=Union[BrokerAResponse, list[BrokerBPosition]],
    summary="Get mock broker data",
    description="Returns mock data for the specified broker.",
)
def get_mock_broker(broker_name: str):
    name = broker_name.lower()
    if name in ("broker-a", "a"):
        return get_broker_a_data()
    elif name in ("broker-b", "b"):
        return get_broker_b_data()
    raise HTTPException(
        status_code=404,
        detail=(
            f"Mock broker source '{broker_name}' not found."
            " Use 'broker-a' or 'broker-b'."
        ),
    )


@app.post(
    "/api/etl-sync",
    response_model=EtlSyncResponse,
    summary="Trigger ETL sync",
    description="Ingests raw broker data, normalizes it, and persists to DynamoDB.",
)
def sync_data():
    return run_etl_sync_logic()


@app.get(
    "/api/positions",
    response_model=list[Position],
    summary="Get all positions",
    description="Returns a list of all positions from the database.",
)
def get_positions():
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


@app.get("/api/positions/{broker}", response_model=list[Position])
def get_positions_by_broker(broker: str):
    response = table.query(KeyConditionExpression=Key("broker").eq(broker))
    items = response.get("Items", [])
    mapped_positions = [map_to_position(item) for item in items]
    if not mapped_positions:
        raise HTTPException(
            status_code=404,
            detail=f"No positions found for broker '{broker}'.",
        )
    return mapped_positions


@app.get("/api/positions/{broker}/{ticker}", response_model=Position)
def get_position(broker: str, ticker: str):
    response = table.get_item(Key={"broker": broker, "ticker": ticker})
    item = response.get("Item")
    if not item:
        raise HTTPException(
            status_code=404,
            detail=(f"Position for broker '{broker}' and ticker '{ticker}' not found."),
        )
    return map_to_position(item)
