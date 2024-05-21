import asyncio
from logging import getLogger
import websockets

logger = getLogger(__name__)


class WebSocketClient:
    def __init__(self, websocket_url: str) -> None:
        self.url = websocket_url
        self.websocket = None
        self.keep_running = True
        self.message_queue = asyncio.Queue()

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.url)
            logger.info(f"WebSocket connection established {self.websocket}")
            asyncio.create_task(self._receive_messages())
        except Exception as e:
            logger.error(f"WebSocket error: {e}")

    async def _receive_messages(self):
        try:
            while self.keep_running:
                message = await self.websocket.recv()
                logger.info(f"Received message: {message}")
                await self.message_queue.put(message)
        except Exception as e:
            logger.error(f"WebSocket error during receive: {e}")
            self.keep_running = False

    async def wait_for_messages(self, count=1, timeout=10):
        messages = []
        try:
            for _ in range(count):
                message = await asyncio.wait_for(self.message_queue.get(), timeout)
                messages.append(message)
        except asyncio.TimeoutError:
            pass
        return messages

    async def close(self):
        self.keep_running = False
        await self.websocket.close()
