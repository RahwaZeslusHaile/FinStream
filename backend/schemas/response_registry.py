from domain.broker import BrokerName
from schemas.brokers import BrokerAResponse, BrokerBResponse

RESPONSE_MAP = {
    BrokerName.broker_a: BrokerAResponse,
    BrokerName.broker_b: BrokerBResponse,
}