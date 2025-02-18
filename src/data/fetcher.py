import ccxt
from src.monitoring.logger import logger

class DataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_data(self):
        """Fetch market data from the exchange."""
        try:
            data = self.exchange.fetch_ohlcv("BTC/USDT", timeframe="1m", limit=100)
            logger.info("Data fetched successfully.")
            return data
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None