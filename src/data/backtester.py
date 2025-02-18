# src/data/backtester.py
import pandas as pd
from typing import Dict
from src.strategies.base_strategy import BaseStrategy
from src.execution.risk_manager import RiskManager
from src.monitoring.logger import logger

class Backtester:
    def __init__(self, strategy: BaseStrategy, initial_balance: float = 10000.0):
        """
        Backtest a strategy on historical data.

        Args:
            strategy (BaseStrategy): Strategy to backtest.
            initial_balance (float): Starting balance in quote currency (e.g., USDT).
        """
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0.0
        self.trades = []

    def run(self, data: pd.DataFrame, params: Dict) -> Dict:
        """
        Run the backtest and return performance metrics.

        Args:
            data (pd.DataFrame): Historical OHLCV data.
            params (Dict): Strategy parameters.

        Returns:
            Dict: Performance report.
        """
        for i in range(1, len(data)):
            current_data = data.iloc[:i]
            signal = self.strategy.generate_signal(current_data, params)

            if signal == "buy" and self.balance > 0:
                self._execute_trade("buy", current_data.iloc[-1]["close"])
            elif signal == "sell" and self.position > 0:
                self._execute_trade("sell", current_data.iloc[-1]["close"])

        return self.generate_report(data)

    def _execute_trade(self, side: str, price: float):
        """Simulate a trade execution."""
        if side == "buy":
            amount = self.balance / price
            self.position += amount
            self.balance = 0.0
        elif side == "sell":
            self.balance = self.position * price
            self.position = 0.0
        self.trades.append({"side": side, "price": price})

    def generate_report(self, data: pd.DataFrame) -> Dict:
        """Generate performance metrics."""
        initial_price = data.iloc[0]["close"]
        final_price = data.iloc[-1]["close"]
        portfolio_value = self.balance + (self.position * final_price)
        return {
            "initial_balance": self.initial_balance,
            "final_balance": portfolio_value,
            "return_pct": (portfolio_value - self.initial_balance) / self.initial_balance * 100,
            "num_trades": len(self.trades),
            "buy_and_hold_return": (final_price - initial_price) / initial_price * 100,
        }