from fastapi import APIRouter

from domain.broker import BrokerName
from schemas.positions import Position
from services.positions import (
    get_all_positions_service,
    get_position_service,
    get_positions_by_broker_service,
)

router = APIRouter(prefix="/api", tags=["positions"])


@router.get(
    "/positions",
    response_model=list[Position],
    summary="Get all positions",
    description="Returns a list of all positions from the database.",
)
def get_all_positions():
    return get_all_positions_service()


@router.get("/positions/{broker}", response_model=list[Position])
def get_positions_by_broker(broker: BrokerName):
    return get_positions_by_broker_service(broker)


@router.get("/positions/{broker}/{ticker}", response_model=Position)
def get_position(broker: BrokerName, ticker: str):
    return get_position_service(broker, ticker)
