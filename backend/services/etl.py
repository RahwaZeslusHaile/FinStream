from datetime import datetime, timezone

from domain.broker import BrokerName
from integrations.s3 import load_raw, save_raw
from mappers.registery import NORMALIZER_REGISTRY
from repositories.etl import delete_all_positions_repo, save_positions_repo
from services.broker_registery import BROKER_REGISTRY


def fetch_broker_data():
    return {
        BrokerName.broker_a: BROKER_REGISTRY[BrokerName.broker_a](),
        BrokerName.broker_b: BROKER_REGISTRY[BrokerName.broker_b](),
    }


def archive_raw_data(data: dict):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    save_raw(
        f"archive/{timestamp}-{BrokerName.broker_a}.json", data[BrokerName.broker_a]
    )
    save_raw(
        f"archive/{timestamp}-{BrokerName.broker_b}.json", data[BrokerName.broker_b]
    )


def load_broker_data(data):
    raw_data = {}
    for broker, payload in data.items():
        loaded = load_raw(f"raw/{broker}.json")
        if loaded is None:
            print(
                f"⚠️ Warning: S3 load failed for {broker}. Falling back to in-memory data."
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
