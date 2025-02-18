# src/tests/test_integration.py
import pytest
from unittest.mock import Mock
from src.core.bot import CryptoBot
from src.execution.exchange import Exchange

@pytest.fixture
def mock_exchange():
    exchange = Mock(spec=Exchange)
    exchange.fetch_ohlcv.return_value = [[1609459200000, 29000, 29500, 28500, 29000, 1000]] * 100
    return exchange

def test_bot_integration(mock_exchange):
    bot = CryptoBot(config={"strategy": "moving_average"}, exchange=mock_exchange)
    bot.run()
    assert mock_exchange.fetch_ohlcv.call_count > 0