# src/strategies/macd.py
import pandas as pd
from src.strategies.base_strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    def generate_signal(self, data: pd.DataFrame, params: Dict[str, Any]) -> str:
        fast_window = params.get("fast_window", 12)
        slow_window = params.get("slow_window", 26)
        signal_window = params.get("signal_window", 9)

        data["ema_fast"] = data["close"].ewm(span=fast_window, adjust=False).mean()
        data["ema_slow"] = data["close"].ewm(span=slow_window, adjust=False).mean()
        data["macd"] = data["ema_fast"] - data["ema_slow"]
        data["signal"] = data["macd"].ewm(span=signal_window, adjust=False).mean()

        if data["macd"].iloc[-1] > data["signal"].iloc[-1]:
            return "buy"
        elif data["macd"].iloc[-1] < data["signal"].iloc[-1]:
            return "sell"
        return "hold"