import json
import logging
import os

import boto3

logger = logging.getLogger(__name__)

s3 = boto3.client("s3")
RAW_DATA_BUCKET = os.getenv("RAW_DATA_BUCKET")


def save_raw(key, data):
    if not RAW_DATA_BUCKET:
        logger.warning("RAW_DATA_BUCKET environment is not set. Skipping S3 upload.")
        return False
    try:
        s3.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=key,
            Body=json.dumps(data),
        )
        return True
    except Exception as e:
        logger.error("Error writing S3 data: %s", e)
        return False


def load_raw(key):
    if not RAW_DATA_BUCKET:
        logger.warning(
            "RAW_DATA_BUCKET environment is not set. Skipping S3 download."
        )
        return None
    try:
        response = s3.get_object(Bucket=RAW_DATA_BUCKET, Key=key)
        data = response["Body"].read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        logger.error("Error reading S3 data: %s", e)
        return None
