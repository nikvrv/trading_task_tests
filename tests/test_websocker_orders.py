import asyncio
import allure
import pytest


@pytest.mark.asyncio
@allure.suite("Websockets")
class TestWebsocket:

    @allure.title("New order message")
    async def test_get_new_order_message(self, websocket_client, new_order):
        await asyncio.sleep(1)
        messages = await websocket_client.get_messages()
        assert messages[0]

    @allure.title("Order executed message")
    async def test_get_order_executed(self, websocket_client, new_order):
        await asyncio.sleep(5)
        messages = await websocket_client.get_messages()
        assert messages[0]

    @allure.title("Delete order message")
    async def test_order_is_deleted(self, websocket_client, delete_order):
        messages = await websocket_client.get_messages()
        assert messages[0]
