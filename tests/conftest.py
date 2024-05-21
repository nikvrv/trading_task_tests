import os

import pytest

from helpers import create_order_data
from src.http_client import HttpClient, HttpMethods
from dotenv import load_dotenv
from src.ws_client import WebSocketClient
import pytest_asyncio

load_dotenv()


class MisconfiguredEnvironment(Exception):
    pass


@pytest.fixture(scope="session")
def config():
    app_url = os.getenv("APP_URL")
    if not app_url:
        raise MisconfiguredEnvironment
    return {"app_url": app_url}


@pytest.fixture
def http_client(config):
    return HttpClient(config["app_url"])


@pytest.fixture
def new_order(http_client):
    data = create_order_data()
    response = http_client.send_request(HttpMethods.POST.value, "/orders", data=data)
    return response.json()


@pytest.fixture
def five_orders(http_client):
    results = []
    for _ in range(5):
        response = http_client.send_request(
            HttpMethods.POST.value, "/orders", data=create_order_data()
        )
        results.append(response.json())
    return results


@pytest_asyncio.fixture(scope='session')
async def websocket_client(config):
    url = "ws://127.0.0.1:8000/ws"
    client = WebSocketClient(url)
    await client.connect()
    yield client
    await client.close()


@pytest.fixture
def delete_order(http_client, new_order):
    http_client.send_request(
        HttpMethods.DELETE, f"/orders/{new_order['id']}"
    )
    return new_order
