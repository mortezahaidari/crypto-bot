# src/core/bot.py
from src.strategies.strategy_factory import StrategyFactory
from src.monitoring.logger import logger

class CryptoBot:
    def __init__(self, config: dict):
        """
        Initialize trading bot with configured strategy
        
        Args:
            config (dict): Loaded configuration from YAML file
        """
        self.config = config
        self._validate_config()
        
        # Initialize strategy through factory
        self.strategy = StrategyFactory.create_strategy(
            self.config['strategy']
        )
        
        # Initialize other components
        self.exchange = self._init_exchange()
        self.risk_manager = RiskManager(config['risk_params'])
        logger.info("Bot initialized with strategy: %s", self.strategy.name)

    def _validate_config(self):
        """Ensure required configuration parameters exist"""
        if 'strategy' not in self.config:
            raise ValueError("Missing 'strategy' section in config")
            
        required_strategy_keys = ['type', 'params']
        if not all(k in self.config['strategy'] for k in required_strategy_keys):
            raise ValueError("Strategy config requires 'type' and 'params' keys")

    def _init_exchange(self):
        """Initialize exchange connection"""
        exchange_config = self.config['exchange']
        return Exchange(
            exchange_id=exchange_config['id'],
            api_key=exchange_config['api_key'],
            api_secret=exchange_config['api_secret']
        )

    def run(self):
        """Main execution loop"""
        # Implementation remains the same