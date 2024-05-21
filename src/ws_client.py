import asyncio
import json
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

    async def send_message(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            await self.websocket.send(message)
            logger.info(f"Message {message} has been sent")
        except websockets.ConnectionClosed:
            logger.error("Cannot send message, WebSocket connection is closed.")
            self.keep_running = False
        except Exception as e:
            logger.error(f"WebSocket error during send: {e}")

    async def get_messages(self) -> list:
        messages = []
        while not self.message_queue.empty():
            messages.append(await self.message_queue.get())
        return messages

    async def wait_for_message(self, timeout=10):
        try:
            return await asyncio.wait_for(self.message_queue.get(), timeout)
        except asyncio.TimeoutError:
            return None

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
