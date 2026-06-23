from datetime import datetime, timezone
from decimal import Decimal

from integrations.dynamodb import table
from integrations.s3 import load_raw, save_raw
from mock.broker import get_broker_a_data, get_broker_b_data


def clear_positions():
    """Scans and clears all existing items from the DynamoDB positions table."""
    print("🧹 Clearing existing positions in DynamoDB...")
    scan_params = {"ProjectionExpression": "broker, ticker"}
    while True:
        response = table.scan(**scan_params)
        items = response.get("Items", [])

        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(
                    Key={"broker": item["broker"], "ticker": item["ticker"]}
                )
        if "LastEvaluatedKey" not in response:
            break
        scan_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]


def run_etl_sync_logic():
    print("📥 Ingesting raw data from mock brokers...")
    dataA = get_broker_a_data()
    dataB = get_broker_b_data()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    save_raw(f"archive/{timestamp}-broker-a.json", dataA)
    save_raw(f"archive/{timestamp}-broker-b.json", dataB)
    save_raw("raw/broker-a.json", dataA)
    save_raw("raw/broker-b.json", dataB)

    print("🔄 Loading raw data from S3 storage layer...")
    raw_a = load_raw("raw/broker-a.json")
    raw_b = load_raw("raw/broker-b.json")

    if raw_a is None:
        print("⚠️ Warning: S3 load failed for Broker A. Falling back to in-memory data.")
        raw_a = dataA
    if raw_b is None:
        print("⚠️ Warning: S3 load failed for Broker B. Falling back to in-memory data.")
        raw_b = dataB

    positions_a = raw_a.get("positions", []) if isinstance(raw_a, dict) else []
    broker_a_name = (
        raw_a.get("source", "Broker_A") if isinstance(raw_a, dict) else "Broker_A"
    )

    if isinstance(raw_b, dict):
        positions_b = raw_b.get("positions", [])
        broker_b_name = raw_b.get("source", "Broker_B")
    else:
        positions_b = raw_b if isinstance(raw_b, list) else []
        broker_b_name = "Broker_B"

    clear_positions()

    print("💾 Writing fresh normalized positions to DynamoDB...")
    positions_added = 0

    with table.batch_writer() as batch:
        for position in positions_a:
            qty = Decimal(str(position["qty"]))
            price = Decimal(str(position["price"]))

            batch.put_item(
                Item={
                    "broker": broker_a_name,
                    "ticker": position["symbol"],
                    "quantity": qty,
                    "market_value": price * qty,
                }
            )
            positions_added += 1

        for position in positions_b:
            qty = Decimal(str(position["amount"]))
            mv = Decimal(str(position["market_value"]))

            batch.put_item(
                Item={
                    "broker": broker_b_name,
                    "ticker": position["ticker"],
                    "quantity": qty,
                    "market_value": mv,
                }
            )
            positions_added += 1

    print(f"✅ ETL Sync Completed. Persisted {positions_added} positions.")
    return {"message": "ETL Sync Completed", "positions_added": positions_added}
