from enum import Enum
import re


class BrokerName(str, Enum):
    broker_a = "broker-a"
    broker_b = "broker-b"


def normalize_broker_name(name: str) -> BrokerName:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name)
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")

    try:
        return BrokerName(normalized)
    except ValueError:
        raise ValueError(f"Unknown broker: {name}")
