# src/execution/paper_exchange.py
class PaperExchange:
    def __init__(self, initial_balance: Dict[str, float] = {"USDT": 10000.0}):
        self.balance = initial_balance.copy()
        self.open_orders = []

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int):
        # Return mock data or historical data
        return [[1609459200000, 29000, 29500, 28500, 29000, 1000]] * limit

    def create_order(self, symbol: str, type: str, side: str, amount: float, price: float = None):
        base, quote = symbol.split('/')
        if side == "buy":
            cost = amount * price
            if self.balance.get(quote, 0) >= cost:
                self.balance[quote] -= cost
                self.balance[base] = self.balance.get(base, 0) + amount
                return {"id": "paper_order_1", "status": "filled"}
        elif side == "sell":
            if self.balance.get(base, 0) >= amount:
                self.balance[base] -= amount
                self.balance[quote] = self.balance.get(quote, 0) + (amount * price)
                return {"id": "paper_order_2", "status": "filled"}
        return None