# src/strategies/rsi.py
import pandas as pd
import numpy as np
from src.strategies.base_strategy import BaseStrategy
# Add this to all strategy files
from typing import Dict, Optional

class RSIStrategy(BaseStrategy):
    def generate_signal(self, data: pd.DataFrame, params: Dict[str, Any]) -> str:
        window = params.get("window", 14)
        overbought = params.get("overbought", 70)
        oversold = params.get("oversold", 30)

        delta = data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        data["rsi"] = rsi

        if rsi.iloc[-1] < oversold:
            return "buy"
        elif rsi.iloc[-1] > overbought:
            return "sell"
        return "hold"