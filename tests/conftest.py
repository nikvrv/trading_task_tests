import os

import pytest
from src.http_client import HttpClient, HttpMethods
from dotenv import load_dotenv

load_dotenv()

class MisconfiguredEnvironment(Exception):
    pass


@pytest.fixture(scope='session')
def config():
    app_url = os.getenv("APP_URL")
    if not app_url:
        raise MisconfiguredEnvironment
    return {"app_url": app_url}


@pytest.fixture
def http_client(config):
    return HttpClient(config['app_url'])


@pytest.fixture
def new_order(http_client):
    data = {
        "stocks": "EURUSD",
        "quantity": 13
    }
    response = http_client.send_request(HttpMethods.POST.value, '/orders', data=data)
    return response.json()

@pytest.fixture
def five_orders(http_client):
    data = {
        "stocks": "EURUSD",
        "quantity": 13
    }
    results = []
    for _ in range(5):
        response = http_client.send_request(HttpMethods.POST.value, '/orders', data=data)
        results.append(response.json())
    return results