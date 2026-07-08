from integrations.dynamodb import table


def delete_all_positions_repo():
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


def save_positions_repo(positions):
    print(f"💾 Persisting {len(positions)} positions to DynamoDB...")

    with table.batch_writer() as batch:
        for pos in positions:
            batch.put_item(
                Item={
                    "broker": pos.broker,
                    "ticker": pos.ticker,
                    "quantity": pos.quantity,
                    "market_value": pos.market_value,
                }
            )

    print(f"✅ Saved {len(positions)} positions to DynamoDB")
