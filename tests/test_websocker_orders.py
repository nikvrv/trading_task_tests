import allure
import pytest
from helpers import extract_dict_from_string


@pytest.mark.asyncio
@allure.suite("Websockets")
class TestWebsocket:
    @allure.title("New order message")
    async def test_get_new_order_message(self, websocket_client, new_order):
        messages = await websocket_client.wait_for_messages()
        message = messages[0]
        assert message.startswith("New order created:")
        order = extract_dict_from_string(message)
        assert order == new_order

    @allure.title("Order executed message")
    async def test_get_order_executed(self, websocket_client, new_order):
        messages = await websocket_client.wait_for_messages(count=2)
        message = messages[-1]
        assert message == f"Order status updated: {new_order['id']} - executed"

    @allure.title("Delete order message")
    async def test_order_is_deleted(self, websocket_client, delete_order):
        messages = await websocket_client.wait_for_messages(count=2)
        message = messages[-1]
        assert message.startswith("Order deleted:")
        order = extract_dict_from_string(message)
        assert order == delete_order
