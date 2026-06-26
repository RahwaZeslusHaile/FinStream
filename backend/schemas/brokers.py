from decimal import Decimal

from pydantic import BaseModel


class BrokerAPosition(BaseModel):
    symbol: str
    qty: Decimal
    price: Decimal


class BrokerAResponse(BaseModel):
    source: str
    positions: list[BrokerAPosition]


class BrokerBPosition(BaseModel):
    ticker: str
    amount: Decimal
    market_value: Decimal
