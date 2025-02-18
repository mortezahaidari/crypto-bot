# src/core/bot.py
import time
from typing import Dict
from src.strategies.strategy_factory import StrategyFactory
from src.monitoring.logger import logger
from src.execution.risk_manager import RiskManager
from src.execution.exchange import Exchange
from src.data.fetcher import DataFetcher

class CryptoBot:
    def __init__(self, config: Dict):
        """
        Professional trading bot with integrated risk management
        
        Args:
            config (dict): Configuration dictionary from YAML
        """
        self.config = config
        self._validate_config()
        
        # Initialize core components
        self.strategy = StrategyFactory.create_strategy(config['strategy'])
        self.exchange = self._init_exchange()
        self.data_fetcher = DataFetcher(self.exchange)
        self.risk_manager = RiskManager(config['risk_params'])
        
        # State tracking
        self.active_positions = {}
        self.trade_history = []
        
        logger.info(f"Bot initialized with strategy: {self.strategy.name}")

    def _validate_config(self) -> None:
        """Validate critical configuration parameters"""
        required_sections = ['strategy', 'exchange', 'risk_params']
        missing = [section for section in required_sections if section not in self.config]
        if missing:
            raise ValueError(f"Missing config sections: {', '.join(missing)}")
            
        if 'interval' not in self.config.get('scheduler', {}):
            raise ValueError("Missing trading interval in scheduler config")

    def _init_exchange(self) -> Exchange:
        """Initialize and verify exchange connection"""
        exchange_config = self.config['exchange']
        exchange = Exchange(
            exchange_id=exchange_config['id'],
            api_key=exchange_config['api_key'],
            api_secret=exchange_config['api_secret']
        )
        
        # Verify connectivity
        try:
            exchange.load_markets()
            logger.info(f"Connected to {exchange_config['id']} exchange")
            return exchange
        except Exception as e:
            logger.error(f"Exchange connection failed: {e}")
            raise

    def execute_strategy(self) -> None:
        """Full trade execution workflow with risk checks"""
        try:
            # 1. Fetch market data
            data = self.data_fetcher.fetch_data(
                symbol=self.config['trading_pair'],
                timeframe=self.config['scheduler']['interval'],
                limit=100
            )
            
            if data.empty:
                logger.warning("No data received, skipping cycle")
                return

            # 2. Generate trading signal
            signal = self.strategy.generate_signal(
                data=data,
                params=self.config['strategy']['params']
            )
            
            if not signal:
                logger.debug("No signal generated")
                return

            # 3. Calculate risk parameters
            current_price = data['close'].iloc[-1]
            stop_loss, take_profit = self.risk_manager.generate_risk_orders(current_price)
            
            position_size = self.risk_manager.calculate_position_size(
                balance=self.exchange.get_balance(self.config['quote_currency']),
                entry_price=current_price,
                stop_loss_price=stop_loss
            )
            
            # 4. Validate trade against risk rules
            if not self.risk_manager.validate_order(
                symbol=self.config['trading_pair'],
                side=signal,
                amount=position_size,
                price=current_price
            ):
                logger.warning("Order blocked by risk manager")
                return

            # 5. Execute trade
            order = self.exchange.place_order(
                symbol=self.config['trading_pair'],
                side=signal,
                amount=position_size,
                order_type='limit',
                price=current_price,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            if order:
                # 6. Update risk state
                self.risk_manager.update_risk_state(
                    pnl=0.0,  # Will update when position closes
                    success=True
                )
                self.active_positions[order['id']] = {
                    'entry_price': current_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
                logger.info(f"Order executed: {order['id']}")

        except Exception as e:
            logger.error(f"Strategy execution failed: {e}")
            self.risk_manager.update_risk_state(pnl=0.0, success=False)

    def run(self) -> None:
        """Main trading loop with graceful shutdown handling"""
        logger.info("Starting trading bot")
        interval = self.config['scheduler'].get('interval', 60)
        
        try:
            while True:
                start_time = time.time()
                
                self.execute_strategy()
                self._monitor_positions()
                
                # Precise sleep timing
                elapsed = time.time() - start_time
                sleep_time = max(interval - elapsed, 1)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully...")
            self._close_all_positions()
        finally:
            logger.info("Trading bot stopped")

    def _monitor_positions(self) -> None:
        """Check open positions and manage risk"""
        for order_id, position in list(self.active_positions.items()):
            try:
                current_price = self.data_fetcher.get_last_price(
                    self.config['trading_pair']
                )
                
                # Check stop loss/take profit
                if current_price <= position['stop_loss']:
                    self.exchange.close_position(order_id, 'stop_loss')
                elif current_price >= position['take_profit']:
                    self.exchange.close_position(order_id, 'take_profit')
                    
            except Exception as e:
                logger.error(f"Position monitoring failed: {e}")

    def _close_all_positions(self) -> None:
        """Close all open positions on shutdown"""
        logger.info("Closing all open positions")
        for order_id in list(self.active_positions.keys()):
            try:
                self.exchange.cancel_order(order_id)
            except Exception as e:
                logger.error(f"Failed to close position {order_id}: {e}")

if __name__ == "__main__":
    from src.config import load_config
    config = load_config()
    bot = CryptoBot(config)
    bot.run()