# src/strategies/base_strategy.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pandas as pd

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: pd.DataFrame, params: Dict[str, Any]) -> Optional[str]:
        """
        Generate trading signal (buy, sell, hold)
        
        Args:
            data: DataFrame containing OHLCV data
            params: Strategy-specific parameters
            
        Returns:
            str: 'buy', 'sell', or None for hold
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique strategy identifier"""
        pass