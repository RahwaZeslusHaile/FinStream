from app import app
from etl.service import run_etl_sync_logic
from integrations.dynamodb import table
from mock.broker import get_broker_a_data, get_broker_b_data


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/mock/broker-a")
def get_broker_a():
    return get_broker_a_data()


@app.get("/mock/broker-b")
def get_broker_b():
    return get_broker_b_data()


@app.post("/api/etl-sync")
def sync_data():
    return run_etl_sync_logic()


@app.get("/api/positions")
def get_positions():
    scan_params = {}
    positions = []
    while True:
        response = table.scan(**scan_params)
        for item in response.get("Items", []):
            positions.append(
                {
                    "broker": item.get("broker"),
                    "ticker": item.get("ticker"),
                    "quantity": item.get("quantity"),
                    "market_value": item.get("market_value"),
                }
            )

        if "LastEvaluatedKey" not in response:
            break
        scan_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]

    return positions
