from boto3.dynamodb.conditions import Key

from integrations.dynamodb import table


def scan_all_positions():
    scan_params = {}
    positions = []

    while True:
        response = table.scan(**scan_params)

        for item in response.get("Items", []):
            positions.append(item)

        if "LastEvaluatedKey" not in response:
            break

        scan_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]

    return positions


def query_positions_by_broker(broker):
    response = table.query(KeyConditionExpression=Key("broker").eq(broker))

    return response.get("Items", [])


def get_position_item(broker, ticker):
    response = table.get_item(
        Key={
            "broker": broker,
            "ticker": ticker,
        }
    )

    return response.get("Item")
