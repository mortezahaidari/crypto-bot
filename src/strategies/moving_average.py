import pandas as pd
from src.strategies.base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, short_window=10, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data):
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["short_ma"] = df["close"].rolling(window=self.short_window).mean()
        df["long_ma"] = df["close"].rolling(window=self.long_window).mean()

        if df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]:
            return "buy"
        elif df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]:
            return "sell"
        return None