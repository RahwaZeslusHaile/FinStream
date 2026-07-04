from fastapi import APIRouter
from domain.broker import BrokerName
from services.brokers import get_broker_service
from schemas.response_registry import RESPONSE_MAP

router = APIRouter(prefix="/api", tags=["brokers"])


@router.get(
    "/brokers/{broker_name}",
    summary="Get broker data",
    description="Returns the data from the specified broker.",
)
def get_broker(broker_name: BrokerName):
    data = get_broker_service(broker_name)
    return RESPONSE_MAP[broker_name].model_validate(data)