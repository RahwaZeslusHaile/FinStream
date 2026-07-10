import logging
from datetime import datetime, timezone

from integrations.s3 import load_raw, save_raw
from mappers.registery import NORMALIZER_REGISTRY
from repositories.etl import delete_all_positions_repo, save_positions_repo
from services.broker_registery import BROKER_REGISTRY

logger = logging.getLogger(__name__)


def fetch_broker_data():
    broker_data = {}
    for broker, fetcher in BROKER_REGISTRY.items():
        if not callable(fetcher):
            broker_data[broker] = None
            logger.warning(
                "Invalid broker configuration for %s: Expected a callable.",
                broker,
            )
            continue
        try:
            broker_data[broker] = fetcher()
        except Exception as e:
            logger.error("Failed to fetch data for %s: %s", broker, e)
            continue
    return broker_data


def archive_raw_data(data: dict):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    for key, value in data.items():
        save_raw(f"archive/{timestamp}-{key}.json", value)


def load_broker_data(data):
    raw_data = {}
    for broker, payload in data.items():
        loaded = load_raw(f"raw/{broker}.json")
        if loaded is None:
            print(
                f"⚠️ Warning: S3 load failed for {broker}."
                " Falling back to in-memory data."
            )
            loaded = payload
        raw_data[broker] = loaded
    return raw_data


def normalize_positions(raw_data):
    positions = []
    for broker, data in raw_data.items():
        normalizer = NORMALIZER_REGISTRY[broker]
        positions.extend(normalizer(data))
    return positions


def run_etl_sync_logic():
    print("📥 Ingesting raw data from mock brokers...")

    broker_data = fetch_broker_data()
    archive_raw_data(broker_data)
    raw_data = load_broker_data(broker_data)
    positions = normalize_positions(raw_data)
    delete_all_positions_repo()
    save_positions_repo(positions)
    return {"message": "ETL Sync Completed", "positions_added": len(positions)}
