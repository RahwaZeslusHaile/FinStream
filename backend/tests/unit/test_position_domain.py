from decimal import Decimal
from domain.broker import BrokerName
from domain.position import consolidate_positions
from schemas.positions import Position


def test_consolidate_positions_sums_duplicates():
    """Test that duplicate positions (same broker & ticker) are summed together."""
    input_positions = [
        Position(broker=BrokerName.broker_a, ticker="AAPL", quantity=Decimal("100"), market_value=Decimal("15000.00")),
        Position(broker=BrokerName.broker_a, ticker="AAPL", quantity=Decimal("50"), market_value=Decimal("7500.00")),
        Position(broker=BrokerName.broker_b, ticker="MSFT", quantity=Decimal("200"), market_value=Decimal("31000.00")),
    ]

    result = consolidate_positions(input_positions)

    assert len(result) == 2
    
    aapl_pos = next(p for p in result if p.ticker == "AAPL")
    assert aapl_pos.quantity == Decimal(str("150"))
    assert aapl_pos.market_value == Decimal(str("22500.00"))
    assert aapl_pos.broker == BrokerName.broker_a

    msft_pos = next(p for p in result if p.ticker == "MSFT")
    assert msft_pos.quantity == Decimal(str("200"))


def test_consolidate_positions_empty_list():
    assert consolidate_positions([]) == []
