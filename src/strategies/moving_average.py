# src/strategies/moving_average.py
import pandas as pd
from src.strategies.base_strategy import BaseStrategy

class MovingAverageCrossover(BaseStrategy):
    def generate_signal(self, data: pd.DataFrame, params: Dict[str, Any]) -> str:
        short_window = params.get("short_window", 10)
        long_window = params.get("long_window", 50)

        data["short_ma"] = data["close"].rolling(window=short_window).mean()
        data["long_ma"] = data["close"].rolling(window=long_window).mean()

        if data["short_ma"].iloc[-1] > data["long_ma"].iloc[-1]:
            return "buy"
        elif data["short_ma"].iloc[-1] < data["long_ma"].iloc[-1]:
            return "sell"
        return "hold"