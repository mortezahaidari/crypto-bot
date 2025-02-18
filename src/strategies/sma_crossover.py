# src/strategies/sma_crossover.py
import pandas as pd
from .base_strategy import BaseStrategy

class SMACrossover(BaseStrategy):
    @property
    def name(self):
        return "sma_crossover"

    def generate_signal(self, data: pd.DataFrame, params: Dict) -> Optional[str]:
        short_window = params.get('short_window', 50)
        long_window = params.get('long_window', 200)
        
        data['sma_short'] = data['close'].rolling(window=short_window).mean()
        data['sma_long'] = data['close'].rolling(window=long_window).mean()
        
        if data['sma_short'].iloc[-1] > data['sma_long'].iloc[-1]:
            return 'buy'
        elif data['sma_short'].iloc[-1] < data['sma_long'].iloc[-1]:
            return 'sell'
        return None