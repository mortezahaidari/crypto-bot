# src/strategies/weighted_strategy.py
from typing import List, Dict
import pandas as pd
from .base_strategy import BaseStrategy

class WeightedStrategy(BaseStrategy):
    def __init__(self, strategies: List[BaseStrategy], weights: List[float]):
        self.strategies = strategies
        self.weights = weights
        
    @property
    def name(self):
        return "weighted_composite"

    def generate_signal(self, data: pd.DataFrame, params: Dict) -> Optional[str]:
        signals = []
        for strategy in self.strategies:
            signal = strategy.generate_signal(data, params)
            signals.append(1 if signal == 'buy' else -1 if signal == 'sell' else 0)
        
        weighted_sum = sum(s * w for s, w in zip(signals, self.weights))
        
        if weighted_sum >= params.get('buy_threshold', 0.7):
            return 'buy'
        elif weighted_sum <= params.get('sell_threshold', -0.7):
            return 'sell'
        return None