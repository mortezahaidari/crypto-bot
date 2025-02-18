# src/data/streamer.py
import websockets
import json
from src.monitoring.logger import logger

class WebSocketStreamer:
    def __init__(self, exchange_url: str):
        self.exchange_url = exchange_url
        self.websocket = None

    async def connect(self):
        """Connect to WebSocket and subscribe to data."""
        self.websocket = await websockets.connect(self.exchange_url)
        logger.info(f"Connected to {self.exchange_url}")

    async def subscribe(self, symbol: str, channel: str = "ticker"):
        """Subscribe to a data channel."""
        msg = json.dumps({
            "method": "SUBSCRIBE",
            "params": [f"{symbol}@{channel}"],
            "id": 1
        })
        await self.websocket.send(msg)
        logger.info(f"Subscribed to {symbol}@{channel}")

    async def stream_data(self, callback):
        """Stream real-time data and pass to callback."""
        while True:
            try:
                data = await self.websocket.recv()
                await callback(json.loads(data))
            except websockets.ConnectionClosed:
                logger.warning("WebSocket disconnected. Reconnecting...")
                await self.connect()