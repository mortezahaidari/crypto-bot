# src/execution/exchange.py
import ccxt
import time
from typing import Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from src.monitoring.logger import logger

class Exchange:
    def __init__(self, exchange_id: str, api_key: str, api_secret: str):
        """
        Advanced exchange wrapper with retries and rate limiting.

        Args:
            exchange_id (str): Exchange ID (e.g., 'binance').
            api_key (str): API key.
            api_secret (str): API secret.
        """
        self.exchange = getattr(ccxt, exchange_id)({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,  # Built-in rate limiting
        })
        logger.info(f"Initialized exchange: {exchange_id}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_ohlcv(self, symbol: str, timeframe: str = "1m", limit: int = 100) -> Optional[List[List]]:
        """
        Fetch OHLCV data with retries for robustness.

        Args:
            symbol (str): Trading pair (e.g., 'BTC/USDT').
            timeframe (str): Timeframe (e.g., '1m').
            limit (int): Number of data points.

        Returns:
            Optional[List[List]]: OHLCV data or None.
        """
        try:
            data = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            logger.debug(f"Fetched {len(data)} OHLCV bars for {symbol}")
            return data
        except ccxt.NetworkError as e:
            logger.warning(f"Network error fetching OHLCV: {e}")
            raise  # Retry on network errors
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def place_order(self, symbol: str, side: str, amount: float, order_type: str = "market") -> Optional[Dict]:
        """
        Place an order with retries and error handling.

        Args:
            symbol (str): Trading pair (e.g., 'BTC/USDT').
            side (str): 'buy' or 'sell'.
            amount (float): Order amount.
            order_type (str): 'market' or 'limit'.

        Returns:
            Optional[Dict]: Order details or None.
        """
        try:
            order = self.exchange.create_order(symbol, order_type, side, amount)
            logger.info(f"Order placed: {order['id']} ({side} {amount} {symbol})")
            return order
        except ccxt.InsufficientFunds as e:
            logger.error(f"Insufficient funds: {e}")
            return None
        except ccxt.NetworkError as e:
            logger.warning(f"Network error placing order: {e}")
            raise
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error: {e}")
            return None

    def get_balance(self, currency: str) -> float:
        """
        Get total balance of a currency.

        Args:
            currency (str): Currency symbol (e.g., 'USDT').

        Returns:
            float: Balance amount.
        """
        balance = self.exchange.fetch_balance()
        return balance["total"].get(currency, 0.0)