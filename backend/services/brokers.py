from domain.broker import BrokerName
from clients.broker_a_client import get_broker_a_data
from clients.broker_b_client import get_broker_b_data
from typing import List, Dict


def get_broker_service(broker_name: BrokerName) -> List[Dict]:
    if broker_name == BrokerName.broker_a:
        return get_broker_a_data()

    if broker_name == BrokerName.broker_b:
        return get_broker_b_data()

    raise ValueError(f"Unknown broker name: {broker_name}")


from domain.broker import BrokerName
from broker_registry import BROKER_REGISTRY


def get_broker_service(broker_name: BrokerName):
    try:
        handler = BROKER_REGISTRY[broker_name]
        return handler()
    except KeyError:
        raise ValueError(f"Unknown broker: {broker_name}")