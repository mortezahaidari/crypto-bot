# src/data/fetcher.py (updated)
class DataFetcher:
    def __init__(self, use_cache: bool = True):
        self.db = DatabaseClient()
        self.use_cache = use_cache

    def fetch_data(self, symbol: str) -> pd.DataFrame:
        # Try to load cached data first
        if self.use_cache:
            cached_data = self.db.load_ohlcv(symbol)
            if not cached_data.empty:
                return cached_data

        # Fetch fresh data if cache is empty
        data = self.exchange.fetch_ohlcv(symbol)
        self.db.save_ohlcv(symbol, data)
        return data