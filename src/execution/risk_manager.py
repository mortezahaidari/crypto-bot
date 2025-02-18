# src/execution/risk_manager.py
import logging
from typing import Dict, Optional, Tuple
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, config: Dict):
        """
        Advanced risk management system with multiple safety mechanisms
        
        Args:
            config (dict): Risk parameters from config.yaml
        """
        # Position sizing parameters
        self.max_position_size = float(config.get("max_position_size", 0.1))  # Max % of portfolio per trade
        self.risk_per_trade = float(config.get("risk_per_trade", 0.01))  # Risk 1% of capital per trade
        
        # Stop loss/take profit
        self.stop_loss_pct = float(config.get("stop_loss_pct", 2.0))  # 2% stop loss
        self.take_profit_pct = float(config.get("take_profit_pct", 3.0))  # 3% take profit
        
        # Circuit breakers
        self.max_daily_drawdown = float(config.get("max_daily_drawdown", 5.0))  # 5% max daily loss
        self.consecutive_loss_limit = int(config.get("consecutive_loss_limit", 3))  # Stop after 3 losses
        
        # State tracking
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.last_trade_time = None
        self.initial_balance = float(config.get("initial_balance", 10000.0))
        self.current_balance = self.initial_balance

    def calculate_position_size(self, entry_price: float, stop_loss_price: float) -> Optional[float]:
        """
        Calculate position size based on risk parameters
        
        Args:
            entry_price: Proposed entry price
            stop_loss_price: Stop loss price
            
        Returns:
            float: Position size in base currency
        """
        try:
            if entry_price <= stop_loss_price:
                logger.error("Stop loss price must be below entry price")
                return None

            risk_per_unit = entry_price - stop_loss_price
            dollar_risk = self.current_balance * self.risk_per_trade
            position_size = dollar_risk / risk_per_unit
            
            # Apply position size limits
            max_size = (self.current_balance * self.max_position_size) / entry_price
            return min(position_size, max_size)
            
        except ZeroDivisionError:
            logger.error("Invalid prices for position sizing")
            return None

    def validate_order(self, symbol: str, side: str, amount: float, price: float) -> bool:
        """
        Validate order against all risk rules
        
        Args:
            symbol: Trading pair
            side: buy/sell
            amount: Order amount
            price: Order price
            
        Returns:
            bool: True if order is allowed
        """
        # Basic validation
        if amount <= 0 or price <= 0:
            logger.warning(f"Invalid order parameters: {amount} {symbol} @ {price}")
            return False

        # Check daily drawdown
        if self.daily_pnl < -self.max_daily_drawdown:
            logger.error(f"Daily drawdown limit reached: {self.daily_pnl:.2f}%")
            return False

        # Check consecutive losses
        if self.consecutive_losses >= self.consecutive_loss_limit:
            logger.error(f"Consecutive loss limit reached: {self.consecutive_losses}")
            return False

        # Check position size
        max_allowed = (self.current_balance * self.max_position_size) / price
        if amount > max_allowed:
            logger.warning(f"Order size {amount:.4f} exceeds max allowed {max_allowed:.4f}")
            return False

        return True

    def update_risk_state(self, pnl: float, success: bool):
        """
        Update risk parameters after completed trade
        
        Args:
            pnl: Profit/loss percentage
            success: Whether trade was successful
        """
        self.current_balance *= (1 + pnl/100)
        self.daily_pnl += pnl
        
        if success:
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1

    def generate_risk_orders(self, entry_price: float) -> Tuple[float, float]:
        """
        Generate stop loss and take profit prices
        
        Args:
            entry_price: Trade entry price
            
        Returns:
            tuple: (stop_loss_price, take_profit_price)
        """
        stop_loss = entry_price * (1 - self.stop_loss_pct/100)
        take_profit = entry_price * (1 + self.take_profit_pct/100)
        return (stop_loss, take_profit)

    def reset_daily_drawdown(self):
        """Reset daily metrics at market close"""
        now = datetime.utcnow()
        if self.last_trade_time and now.date() > self.last_trade_time.date():
            self.daily_pnl = 0.0
            self.initial_balance = self.current_balance
            logger.info("Daily metrics reset")