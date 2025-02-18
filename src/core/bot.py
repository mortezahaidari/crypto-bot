import schedule
import time
from src.data.fetcher import DataFetcher
from src.strategies.base_strategy import BaseStrategy
from src.execution.order_manager import OrderManager
from src.monitoring.logger import logger

class CryptoBot:
    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy
        self.data_fetcher = DataFetcher()
        self.order_manager = OrderManager()

    def run(self):
        """Run the bot on a schedule."""
        schedule.every(1).minutes.do(self.execute_strategy)
        logger.info("Bot started.")
        while True:
            schedule.run_pending()
            time.sleep(1)

    def execute_strategy(self):
        """Fetch data, execute strategy, and place orders."""
        data = self.data_fetcher.fetch_data()
        signal = self.strategy.generate_signal(data)
        if signal:
            self.order_manager.place_order(signal)