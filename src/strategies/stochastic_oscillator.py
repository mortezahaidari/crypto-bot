# src/strategies/stochastic_oscillator.py
import pandas as pd
from .base_strategy import BaseStrategy

class StochasticOscillator(BaseStrategy):
    @property
    def name(self):
        return "stochastic_oscillator"

    def generate_signal(self, data: pd.DataFrame, params: Dict) -> Optional[str]:
        k_period = params.get('k_period', 14)
        d_period = params.get('d_period', 3)
        overbought = params.get('overbought', 80)
        oversold = params.get('oversold', 20)
        
        low_min = data['low'].rolling(window=k_period).min()
        high_max = data['high'].rolling(window=k_period).max()
        
        data['%K'] = 100 * ((data['close'] - low_min) / (high_max - low_min))
        data['%D'] = data['%K'].rolling(window=d_period).mean()
        
        if data['%K'].iloc[-1] < oversold and data['%D'].iloc[-1] < oversold:
            return 'buy'
        elif data['%K'].iloc[-1] > overbought and data['%D'].iloc[-1] > overbought:
            return 'sell'
        return None