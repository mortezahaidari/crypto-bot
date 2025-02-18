# src/strategies/bollinger_bands.py
import pandas as pd
from src.strategies.base_strategy import BaseStrategy
# Add this to all strategy files
from typing import Dict, Optional, Any

class BollingerBandsStrategy(BaseStrategy):
    def generate_signal(self, data: pd.DataFrame, params: Dict[str, Any]) -> str:
        window = params.get("window", 20)
        num_std = params.get("num_std", 2)

        data["ma"] = data["close"].rolling(window=window).mean()
        data["std"] = data["close"].rolling(window=window).std()
        data["upper_band"] = data["ma"] + (data["std"] * num_std)
        data["lower_band"] = data["ma"] - (data["std"] * num_std)

        if data["close"].iloc[-1] < data["lower_band"].iloc[-1]:
            return "buy"
        elif data["close"].iloc[-1] > data["upper_band"].iloc[-1]:
            return "sell"
        return "hold"