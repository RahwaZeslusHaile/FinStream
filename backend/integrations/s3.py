import json
import os

import boto3

s3 = boto3.client("s3")
RAW_DATA_BUCKET = os.getenv("RAW_DATA_BUCKET")


def save_raw(key, data):
    if not RAW_DATA_BUCKET:
        print("⚠️ Warning: RAW_DATA_BUCKET environment is not set. Skipping S3 upload.")
        return False
    try:
        s3.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=key,
            Body=json.dumps(data),
        )
        return True
    except Exception as e:
        print(f"Error writing S3 data: {e}")
        return False


def load_raw(key):
    if not RAW_DATA_BUCKET:
        print(
            "⚠️ Warning: RAW_DATA_BUCKET environment is not set. Skipping S3 download."
        )
        return None
    try:
        response = s3.get_object(Bucket=RAW_DATA_BUCKET, Key=key)
        data = response["Body"].read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        print(f"Error reading S3 data: {e}")
        return None
