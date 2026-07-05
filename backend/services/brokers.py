from domain.broker import BrokerName
from services.broker_registery import BROKER_REGISTRY


def get_broker_service(broker_name: BrokerName):
    try:
        handler = BROKER_REGISTRY[broker_name]
        return handler()
    except KeyError:
        raise ValueError(f"Unknown broker: {broker_name}")
