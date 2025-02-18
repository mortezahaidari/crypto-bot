# src/data/storage.py
import sqlite3
import pandas as pd
from src.monitoring.logger import logger

class DatabaseClient:
    def __init__(self, db_path: str = "data/crypto_data.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ohlcv (
                timestamp INTEGER PRIMARY KEY,
                symbol TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        """)

    def save_ohlcv(self, symbol: str, data: pd.DataFrame):
        """Cache OHLCV data to SQLite."""
        data["symbol"] = symbol
        data.to_sql("ohlcv", self.conn, if_exists="append", index=False)
        logger.debug(f"Cached {len(data)} bars for {symbol}")

    def load_ohlcv(self, symbol: str, limit: int = 1000) -> pd.DataFrame:
        """Load cached OHLCV data."""
        query = f"""
            SELECT * FROM ohlcv
            WHERE symbol = '{symbol}'
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        return pd.read_sql(query, self.conn)