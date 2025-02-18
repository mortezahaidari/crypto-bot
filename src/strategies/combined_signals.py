# src/strategies/combined_signals.py
from typing import List, Dict
import pandas as pd
from .base_strategy import BaseStrategy
# Add this to all strategy files
from typing import Dict, Optional

class CombinedStrategy(BaseStrategy):
    def __init__(self, strategies: List[BaseStrategy]):
        self.strategies = strategies
        
    @property
    def name(self):
        return "combined_signals"

    def generate_signal(self, data: pd.DataFrame, params: Dict) -> Optional[str]:
        signals = []
        for strategy in self.strategies:
            signal = strategy.generate_signal(data, params)
            signals.append(signal)
            
        buy_signals = signals.count('buy')
        sell_signals = signals.count('sell')
        
        if buy_signals >= params.get('consensus_threshold', 2):
            return 'buy'
        elif sell_signals >= params.get('consensus_threshold', 2):
            return 'sell'
        return None