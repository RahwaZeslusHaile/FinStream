import logging
from datetime import datetime, timezone

from integrations.s3 import load_raw, save_raw
from mappers.registery import NORMALIZER_REGISTRY
from repositories.etl import delete_all_positions_repo, save_positions_repo
from schemas.positions import Position
from services.broker_registery import BROKER_REGISTRY

logger = logging.getLogger(__name__)


def fetch_broker_data() -> tuple[dict, dict]:
    broker_data = {}
    failed_brokers = {}
    for broker, fetcher in BROKER_REGISTRY.items():
        if not callable(fetcher):
            failed_brokers[broker] = "Invalid Broker Configuration"
            logger.warning(
                "Invalid broker configuration for %s: Expected a callable.", broker
            )
            continue
        try:
            broker_data[broker] = fetcher()
        except Exception as e:
            logger.error("Failed to fetch data for %s: %s", broker, e)
            failed_brokers[broker] = str(e)
            continue

    return broker_data, failed_brokers


def archive_raw_data(data: dict) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    for broker, payload in data.items():
        save_raw(f"archive/{timestamp}-{broker}.json", payload)
        save_raw(f"raw/{broker}.json", payload)


def load_broker_data(data: dict) -> dict:
    raw_data = {}
    for broker, payload in data.items():
        loaded = load_raw(f"raw/{broker}.json")
        if loaded is None:
            logger.warning(
                "Warning: S3 load failed for %s. Falling back to in-memory data.",
                broker,
            )
            loaded = payload
        raw_data[broker] = loaded
    return raw_data


def normalize_positions(raw_data: dict) -> tuple[list[Position], dict]:
    normalized_positions = []
    failed_normalizers = {}
    for broker, data in raw_data.items():
        normalizer = NORMALIZER_REGISTRY.get(broker)
        if normalizer is None:
            failed_normalizers[broker] = "No normalizer found for broker"
            continue
        try:
            positions = normalizer(data)
            normalized_positions.extend(positions)
        except Exception as e:
            failed_normalizers[broker] = str(e)
            logger.exception("Failed to normalize data for %s", broker)
    return normalized_positions, failed_normalizers


def run_etl_sync_logic():
    logger.info("fetching broker data...")
    try:
        broker_data, failed_brokers = fetch_broker_data()
        if failed_brokers:
            return {
                "message": "ETL Sync Aborted. Some brokers failed to fetch data",
                "failed_brokers": failed_brokers,
                "positions_added": 0,
            }
        logger.info("Fetched data for %s", broker_data.keys())

        logger.info("Archiving raw data...")
        archive_raw_data(broker_data)
        logger.info("Archived raw data")

        logger.info("Loading raw data...")
        raw_data = load_broker_data(broker_data)
        logger.info("Loaded raw data")

        logger.info("Normalizing positions...")
        positions, failed_normalizers = normalize_positions(raw_data)
        if failed_normalizers:
            logger.warning(
                "Warning: Normalization failed for %s. Continuing with other brokers.",
                failed_normalizers,
            )
        if not positions:
            logger.warning("ETL sync aborted. No positions normalized.")
            return {
                "message": "ETL Sync Aborted. No positions normalized",
                "positions_added": 0,
            }
        logger.info("Saving %s positions", len(positions))
        delete_all_positions_repo()
        logger.info("Deleted all positions")

        logger.info("Saving %s positions...", len(positions))
        save_positions_repo(positions)
        logger.info("Saved %s positions", len(positions))

        return {"message": "ETL Sync Completed", "positions_added": len(positions)}

    except Exception as e:
        logger.exception("ETL sync failed unexpectedly: %s", e)
        return {"message": "ETL Sync Failed", "error": str(e), "positions_added": 0}
