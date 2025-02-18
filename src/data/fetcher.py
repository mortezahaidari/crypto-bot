# Add this at the top of the file
import pandas as pd

class DataFetcher:
    def __init__(self, exchange):
        self.exchange = exchange

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        """Fetch OHLCV data and return as DataFrame"""
        try:
            data = self.exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
            return pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        except Exception as e:
            print(f"Data fetch error: {e}")
            return pd.DataFrame()  # Return empty DF instead of None