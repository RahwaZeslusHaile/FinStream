from fastapi import APIRouter

from domain.broker import BrokerName
from schemas.response_registry import RESPONSE_MAP
from services.brokers import get_broker_service

router = APIRouter(prefix="/api", tags=["brokers"])


@router.get(
    "/brokers/{broker_name}",
    summary="Get broker data",
    description="Returns the data from the specified broker.",
)
def get_broker(broker_name: BrokerName):
    data = get_broker_service(broker_name)
    return RESPONSE_MAP[broker_name].model_validate(data)
