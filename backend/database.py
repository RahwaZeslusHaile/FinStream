import os

import boto3

TABLE_NAME = os.getenv("TABLE_NAME","finstream-positions")
REGION = os.getenv("REGION_NAME", "us-east-1")
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


