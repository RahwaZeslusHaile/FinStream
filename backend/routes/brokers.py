from fastapi import APIRouter

from domain.broker import BrokerName, normalize_broker_name
from schemas.response_registry import RESPONSE_MAP
from services.brokers import get_broker_service

router = APIRouter(prefix="/api", tags=["brokers"])


@router.get(
    "/brokers/{broker_name}",
    summary="Get broker data",
    description="Returns the data from the specified broker.",
)
def get_broker(broker_name: str):
    normalized_name = normalize_broker_name(broker_name)
    data = get_broker_service(normalized_name)
    return RESPONSE_MAP[normalized_name].model_validate(data)
