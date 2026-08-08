import logging

from integrations.dynamodb import table

logger = logging.getLogger(__name__)


def delete_all_positions_repo():
    logger.info("Clearing existing positions in DynamoDB...")
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
    logger.info("Persisting %s positions to DynamoDB...", len(positions))

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

    logger.info("Saved %s positions to DynamoDB", len(positions))
