import pytest
from src.strategies.moving_average import MovingAverageStrategy

def test_moving_average_strategy():
    strategy = MovingAverageStrategy()
    data = [[1609459200000, 29000, 29500, 28500, 29000, 1000]] * 100
    signal = strategy.generate_signal(data)
    assert signal in ["buy", "sell", None]
    

# src/tests/test_strategies.py
def test_rsi_strategy():
    data = pd.DataFrame({"close": [100, 101, 102, 101, 100, 99, 98, 97, 96, 95]})
    strategy = RSIStrategy()
    signal = strategy.generate_signal(data, {"window": 14, "oversold": 30, "overbought": 70})
    assert signal in ["buy", "sell", "hold"]    