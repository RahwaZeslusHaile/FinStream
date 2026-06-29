from decimal import Decimal

from pydantic import BaseModel


class Position(BaseModel):
    broker: str
    ticker: str
    quantity: Decimal
    market_value: Decimal
