from domain.broker import BrokerName
from mappers.broker_a import normalize_broker_a
from mappers.broker_b import normalize_broker_b

NORMALIZER_REGISTRY = {
    BrokerName.broker_a: normalize_broker_a,
    BrokerName.broker_b: normalize_broker_b,
}
