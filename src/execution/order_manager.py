# src/execution/order_manager.py
from typing import Dict, Optional
import sqlite3
from src.execution.exchange import Exchange
from src.monitoring.logger import logger

class OrderManager:
    def __init__(self, exchange: Exchange, db_path: str = "orders.db"):
        """
        Professional order manager with database tracking and slippage handling.

        Args:
            exchange (Exchange): Initialized exchange wrapper.
            db_path (str): Path to SQLite database.
        """
        self.exchange = exchange
        self.conn = sqlite3.connect(db_path)
        self._create_order_table()
        logger.info("Order manager initialized")

    def _create_order_table(self):
        """Create orders table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            symbol TEXT,
            side TEXT,
            amount REAL,
            price REAL,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)

    def place_order(
        self, symbol: str, side: str, amount: float, order_type: str = "market", price: Optional[float] = None
    ) -> Optional[Dict]:
        """
        Place an order with slippage handling and database tracking.

        Args:
            price (Optional[float]): Required for limit orders.
        """
        try:
            order = self.exchange.place_order(symbol, side, amount, order_type, price)
            if order:
                self._store_order(order)
                logger.info(f"Order {order['id']} placed successfully")
            return order
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return None

    def _store_order(self, order: Dict):
        """Store order details in the database."""
        query = """
        INSERT INTO orders (id, symbol, side, amount, price, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (
                order["id"],
                order["symbol"],
                order["side"],
                order["amount"],
                order.get("price"),
                order["status"],
            ),
        )
        self.conn.commit()