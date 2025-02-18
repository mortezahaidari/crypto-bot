# src/strategies/strategy_factory.py
from typing import Dict, Any
from .base_strategy import BaseStrategy
from .sma_crossover import SMACrossover
from .atr_filter import ATRFilter
from .stochastic_oscillator import StochasticOscillator
from .moving_average import MovingAverageCrossover
from .combined_signals import CombinedStrategy
from .weighted_strategy import WeightedStrategy

class StrategyFactory:
    _registry = {
        'sma_crossover': SMACrossover,
        'atr_filter': ATRFilter,
        'stochastic': StochasticOscillator,
        'moving_average': MovingAverageCrossover,
        'combined': CombinedStrategy,
        'weighted': WeightedStrategy
    }

    @classmethod
    def create_strategy(cls, strategy_config: Dict[str, Any]) -> BaseStrategy:
        strategy_type = strategy_config['type']
        
        if strategy_type not in cls._registry:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
            
        strategy_class = cls._registry[strategy_type]
        
        # Handle composite strategies
        if strategy_type in ['combined', 'weighted']:
            sub_strategies = [
                cls.create_strategy(sub_config) 
                for sub_config in strategy_config.get('strategies', [])
            ]
            if strategy_type == 'weighted':
                return strategy_class(
                    strategies=sub_strategies,
                    weights=strategy_config.get('weights', [])
                )
            return strategy_class(sub_strategies)
            
        return strategy_class()