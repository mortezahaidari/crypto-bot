import pytest
from src.strategies.moving_average import MovingAverageStrategy

def test_moving_average_strategy():
    strategy = MovingAverageStrategy()
    data = [[1609459200000, 29000, 29500, 28500, 29000, 1000]] * 100
    signal = strategy.generate_signal(data)
    assert signal in ["buy", "sell", None]