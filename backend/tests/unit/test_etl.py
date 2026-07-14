from unittest.mock import patch

import pytest

from domain.broker import BrokerName
from schemas.positions import Position
from services.etl import run_etl_sync_logic


@pytest.fixture
def mock_etl_dependencies():
    with (
        patch("services.etl.BROKER_REGISTRY", {}) as mock_broker_registry,
        patch("services.etl.NORMALIZER_REGISTRY", {}) as mock_normalizer_registry,
        patch("services.etl.save_raw") as mock_save_raw,
        patch("services.etl.load_raw") as mock_load_raw,
        patch("services.etl.delete_all_positions_repo") as mock_delete_repo,
        patch("services.etl.save_positions_repo") as mock_save_repo,
    ):
        yield {
            "broker_registry": mock_broker_registry,
            "normalizer_registry": mock_normalizer_registry,
            "save_raw": mock_save_raw,
            "load_raw": mock_load_raw,
            "delete_all_positions_repo": mock_delete_repo,
            "save_positions_repo": mock_save_repo,
        }


def test_run_etl_sync_success(mock_etl_dependencies):
    deps = mock_etl_dependencies

    deps["broker_registry"][BrokerName.broker_a] = lambda: {"raw": "data"}

    mock_position = Position(
        broker="broker-a",
        ticker="AAPL",
        quantity=10,
        market_value=2000,
    )
    deps["normalizer_registry"][BrokerName.broker_a] = lambda data: [mock_position]

    deps["load_raw"].return_value = {"raw": "data"}

    result = run_etl_sync_logic()
    assert result["message"] == "ETL Sync Completed"
    assert result["positions_added"] == 1

    deps["delete_all_positions_repo"].assert_called_once()
    deps["save_positions_repo"].assert_called_once_with([mock_position])


def test_run_etl_sync_fetch_failure(mock_etl_dependencies):
    deps = mock_etl_dependencies

    def failing_fetcher():
        raise Exception("Connection timed out")

    deps["broker_registry"][BrokerName.broker_a] = failing_fetcher
    result = run_etl_sync_logic()

    assert "Aborted" in result["message"]
    assert result["positions_added"] == 0
    assert result["failed_brokers"]["broker-a"] == "Connection timed out"

    deps["delete_all_positions_repo"].assert_not_called()
    deps["save_positions_repo"].assert_not_called()


def test_run_etl_sync_normalization_failure(mock_etl_dependencies):
    deps = mock_etl_dependencies

    deps["broker_registry"][BrokerName.broker_a] = lambda: {"raw": "data"}

    def failing_normalizer(data):
        raise ValueError("Invalid symbol format")

    deps["normalizer_registry"][BrokerName.broker_a] = failing_normalizer

    deps["load_raw"].return_value = {"raw": "data"}

    result = run_etl_sync_logic()

    assert "Aborted" in result["message"]
    assert result["positions_added"] == 0
    assert result["failed_normalizers"]["broker-a"] == "Invalid symbol format"

    deps["delete_all_positions_repo"].assert_not_called()
    deps["save_positions_repo"].assert_not_called()
