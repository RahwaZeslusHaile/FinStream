"""ETL synchronization service for broker portfolio data.

This module coordinates the extraction, transformation, and loading (ETL)
of financial positions from various configured brokers, archiving raw payloads
to S3, and persisting normalized data to DynamoDB.
"""

import logging
from datetime import datetime, timezone

from domain.broker import BrokerName, normalize_broker_name
from integrations.s3 import load_raw, save_raw
from mappers.registery import NORMALIZER_REGISTRY
from repositories.etl import delete_all_positions_repo, save_positions_repo
from schemas.positions import Position
from services.broker_registery import BROKER_REGISTRY

logger = logging.getLogger(__name__)


def get_canonical_broker(
    broker: BrokerName | str,
) -> BrokerName:
    """Normalizes a broker input into its canonical BrokerName enum member.

    Args:
        broker: The broker name as a string or a BrokerName enum instance.

    Returns:
        The canonical BrokerName enum member.

    Raises:
        ValueError: If the broker name cannot be recognized or is invalid.
    """
    if isinstance(broker, BrokerName):
        return broker

    return normalize_broker_name(broker)


def fetch_broker_data() -> tuple[dict[BrokerName, dict], dict]:
    """Fetches raw portfolio payloads from all registered brokers.

    Iterates through the registered brokers in the global registry and calls
    their respective data-fetching routines.

    Returns:
        A tuple of two dictionaries:
            - broker_data: Successfully fetched payloads keyed by canonical BrokerName.
            - failed_brokers: Error messages keyed by the broker string name.
    """
    broker_data = {}
    failed_brokers = {}

    for broker, fetcher in BROKER_REGISTRY.items():
        try:
            canonical_broker = get_canonical_broker(broker)

        except ValueError as e:
            failed_brokers[str(broker)] = str(e)
            logger.error(
                "Invalid broker name %s: %s",
                broker,
                e,
            )
            continue

        if canonical_broker in broker_data:
            failed_brokers[canonical_broker.value] = "Duplicate broker registration"
            logger.error(
                "Duplicate broker registration detected: %s",
                canonical_broker.value,
            )
            continue

        if not callable(fetcher):
            failed_brokers[canonical_broker.value] = "Fetcher is not callable"
            logger.error(
                "Invalid fetcher configuration for %s",
                canonical_broker.value,
            )
            continue

        try:
            broker_data[canonical_broker] = fetcher()

        except Exception as e:
            failed_brokers[canonical_broker.value] = str(e)
            logger.exception(
                "Failed fetching data for %s",
                canonical_broker.value,
            )

    return broker_data, failed_brokers


def archive_raw_data(
    data: dict[BrokerName, dict],
) -> None:
    """Saves raw broker payloads to Amazon S3 for archival and tracking.

    Uploads a timestamped copy of each payload to `archive/` and overwrites
    the active raw payload file under `raw/`.

    Args:
        data: A dictionary mapping canonical BrokerName to raw payload data.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    for broker, payload in data.items():
        broker_name = broker.value

        save_raw(
            f"archive/{timestamp}-{broker_name}.json",
            payload,
        )

        save_raw(
            f"raw/{broker_name}.json",
            payload,
        )


def load_broker_data(
    data: dict[BrokerName, dict],
) -> dict[BrokerName, dict]:
    """Loads raw broker payloads from S3, falling back to in-memory data on failure.

    Attempts to pull the recently archived `raw/` files from S3 to ensure
    persistence state parity. If S3 fails or is unconfigured, it logs a warning
    and defaults to the in-memory payloads passed in.

    Args:
        data: In-memory dictionary of canonical BrokerName to fetched payloads.

    Returns:
        A dictionary of broker payloads loaded from S3 (or the fallback).
    """
    raw_data = {}

    for broker, payload in data.items():
        loaded = load_raw(f"raw/{broker.value}.json")

        if loaded is None:
            logger.warning(
                "S3 load failed for %s. Using memory fallback.",
                broker.value,
            )

            loaded = payload

        raw_data[broker] = loaded

    return raw_data


def normalize_positions(
    raw_data: dict[BrokerName, dict],
) -> tuple[list[Position], dict]:
    """Transforms raw broker JSON data into standardized Position models.

    Args:
        raw_data: Raw JSON payloads from each broker.

    Returns:
        A tuple of:
            - list[Position]: Standardized Position model instances.
            - dict[BrokerName, str]: Normalizer failure messages keyed by BrokerName.
    """
    normalized_positions = []
    failed_normalizers = {}

    for broker, data in raw_data.items():
        normalizer = NORMALIZER_REGISTRY.get(broker)

        if normalizer is None:
            logger.error(
                "No normalizer registered for %s",
                broker.value,
            )

            failed_normalizers[broker] = "No normalizer found"

            continue

        try:
            positions = normalizer(data)

            normalized_positions.extend(positions)

        except Exception as e:
            logger.exception(
                "Normalization failed for %s",
                broker.value,
            )

            failed_normalizers[broker] = str(e)

    return normalized_positions, failed_normalizers


def run_etl_sync_logic():
    """Orchestrates the entire ETL synchronization workflow.

    Executes the pipeline in sequential phases:
        1. Fetch raw data from all brokers.
        2. Archive raw payloads to S3.
        3. Reload/verify broker data from S3.
        4. Normalize raw payloads into standardized Position schema items.
        5. Purge the existing active positions table in DynamoDB.
        6. Persist normalized positions to DynamoDB.

    Returns:
        A dictionary containing an execution summary "message", list of
        failed normalizers or brokers if aborted, and count of "positions_added".
    """
    logger.info("Starting ETL synchronization")

    try:
        broker_data, failed_brokers = fetch_broker_data()

        if failed_brokers:
            logger.error(
                "ETL aborted during broker fetch: %s",
                failed_brokers,
            )

            return {
                "message": ("ETL Sync Aborted. Broker fetch failed"),
                "failed_brokers": failed_brokers,
                "positions_added": 0,
            }

        if not broker_data:
            return {
                "message": ("ETL Sync Aborted. No broker data"),
                "positions_added": 0,
            }


        logger.info("Archiving raw broker payloads")

        archive_raw_data(broker_data)

        raw_data = load_broker_data(broker_data)

        logger.info("Normalizing positions...")
        positions, failed_normalizers = normalize_positions(raw_data)

        if failed_normalizers:
            logger.error(
                "ETL Aborted. Failed to normalize position data for the following brokers: %s",
                failed_normalizers,
            )

            return {
                "message": ("ETL Sync Aborted. Normalization failed"),
                "failed_normalizers": failed_normalizers,
                "positions_added": 0,
            }

        if not positions:
            logger.warning("No positions created after normalization")

            return {
                "message": ("ETL Sync Aborted. No positions"),
                "positions_added": 0,
            }

        logger.info("Deleting old positions")

        delete_all_positions_repo()

        logger.info(
            "Saving %s positions",
            len(positions),
        )

        save_positions_repo(positions)

        logger.info("ETL completed successfully")

        return {
            "message": "ETL Sync Completed",
            "positions_added": len(positions),
        }

    except Exception as e:
        logger.exception("Unexpected ETL failure")

        return {
            "message": "ETL Sync Failed",
            "error": str(e),
            "positions_added": 0,
        }
