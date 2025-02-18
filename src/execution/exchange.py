import ccxt
import time
from typing import Dict, List, Optional
from src.monitoring.logger import logger

class Exchange:
    def __init__(self, exchange_id: str, api_key: str, api_secret: str):
        """
        Initialize the exchange wrapper.

        :param exchange_id: ID of the exchange (e.g., 'binance').
        :param api_key: API key for the exchange.
        :param api_secret: API secret for the exchange.
        """
        self.exchange = getattr(ccxt, exchange_id)({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,  # Enable rate limiting to avoid API bans
        })
        logger.info(f"Initialized exchange: {exchange_id}")

    def fetch_ohlcv(self, symbol: str, timeframe: str = "1m", limit: int = 100) -> Optional[List[List]]:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data.

        :param symbol: Trading pair (e.g., 'BTC/USDT').
        :param timeframe: Timeframe for the data (e.g., '1m', '1h').
        :param limit: Number of data points to fetch.
        :return: List of OHLCV data or None if an error occurs.
        """
        try:
            data = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            logger.info(f"Fetched OHLCV data for {symbol} ({timeframe})")
            return data
        except Exception as e:
            logger.error(f"Error fetching OHLCV data for {symbol}: {e}")
            return None

    def place_order(self, symbol: str, side: str, amount: float, order_type: str = "market") -> Optional[Dict]:
        """
        Place an order on the exchange.

        :param symbol: Trading pair (e.g., 'BTC/USDT').
        :param side: Order side ('buy' or 'sell').
        :param amount: Amount to buy/sell.
        :param order_type: Type of order ('market' or 'limit').
        :return: Order details or None if an error occurs.
        """
        try:
            order = self.exchange.create_order(symbol, order_type, side, amount)
            logger.info(f"Placed {side} order for {amount} {symbol}")
            return order
        except Exception as e:
            logger.error(f"Error placing {side} order for {amount} {symbol}: {e}")
            return None

    def get_balance(self, currency: str) -> Optional[float]:
        """
        Get the balance of a specific currency.

        :param currency: Currency symbol (e.g., 'BTC', 'USDT').
        :return: Balance amount or None if an error occurs.
        """
        try:
            balance = self.exchange.fetch_balance()
            return balance["total"].get(currency, 0.0)
        except Exception as e:
            logger.error(f"Error fetching balance for {currency}: {e}")
            return None