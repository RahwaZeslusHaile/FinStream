from fastapi import APIRouter

from schemas.etl import EtlSyncResponse
from services.etl import run_etl_sync_logic

router = APIRouter(prefix="/api", tags=["Etl"])


@router.post(
    "/etl-sync",
    response_model=EtlSyncResponse,
    summary="Trigger ETL sync",
    description="Ingests raw broker data, normalizes it, and persists to DynamoDB.",
)
def sync_data():
    return run_etl_sync_logic()
