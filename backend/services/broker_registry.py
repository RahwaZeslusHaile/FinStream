from clients.broker_a_client import get_broker_a_data
from clients.broker_b_client import get_broker_b_data
from domain.broker import BrokerName

BROKER_REGISTRY = {
    BrokerName.broker_a: get_broker_a_data,
    BrokerName.broker_b: get_broker_b_data,
}
