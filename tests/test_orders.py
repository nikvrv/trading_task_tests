import random
import time

import pytest
import allure

from helpers import create_order_data, get_random_int
from src.http_client import HttpMethods
from src.models import Order


@allure.suite(HttpMethods.POST.value)
class TestPostOrders:
    ENDPOINT = "/orders"

    @allure.title("Create an order")
    def test_create_order(self, http_client):
        data = create_order_data()
        response = http_client.send_request(HttpMethods.POST, self.ENDPOINT, data=data)
        assert response.status_code == 201, "Wrong status code"
        order = Order(**response.json())

        assert order.stocks == data['stocks']
        assert order.quantity == data['quantity']
        assert order.status == "pending"

    @allure.title("Create order invalid data")
    def test_create_order_invalid_data(self, http_client):
        response = http_client.send_request(HttpMethods.POST, self.ENDPOINT, data={})
        assert response.status_code == 400, "Wrong status code"


@allure.suite(HttpMethods.GET.value)
class TestGetOrders:
    ENDPOINT = "/orders"
    ERROR_MESSAGE = {"detail": "Order not found"}

    @allure.title("Get order")
    def test_get_order(self, http_client, new_order):
        response = http_client.send_request(
            HttpMethods.GET, f"{self.ENDPOINT}/{new_order['id']}"
        )
        assert response.status_code == 200, "Wrong status code"
        assert new_order == response.json(), "Order is not equal"

    @allure.title("Get not exists order")
    def test_get_not_exist_order(self, http_client):
        random_id = random.randint(999, 9999)
        response = http_client.send_request(
            HttpMethods.GET, f"{self.ENDPOINT}/{random_id}"
        )
        assert response.status_code == 404, "Wrong status code"
        assert response.json() == self.ERROR_MESSAGE, "Error message is wrong"

    @allure.title("Get order with invalid data")
    @pytest.mark.parametrize("wrong_data", ("1.1", [], "123"))
    def test_get_order_invalid_data(self, http_client, wrong_data):
        response = http_client.send_request(
            HttpMethods.GET, f"{self.ENDPOINT}/{wrong_data}"
        )
        assert response.status_code == 404, "Wrong status code"
        assert response.json() == self.ERROR_MESSAGE, "Error message is wrong"

    @allure.title("Get all orders")
    def test_get_orders(self, http_client, five_orders):
        response = http_client.send_request(HttpMethods.GET, f"{self.ENDPOINT}")
        assert response.status_code == 200, "Wrong status code"
        assert five_orders in response.json(), "Orders not in results"


@allure.suite(HttpMethods.DELETE.value)
class TestDeleteOrder:
    ENDPOINT = "/orders"
    ERROR_MESSAGE = {"detail": "Order not found"}

    @allure.title("Delete order")
    def test_delete_order(self, http_client, new_order):
        response = http_client.send_request(
            HttpMethods.DELETE, f"{self.ENDPOINT}/{new_order['id']}"
        )
        assert response.status_code == 204, "Wrong status code"
        assert response.text == ""

    @allure.title("Delete not exists order")
    def test_delete_not_exists_order(self, http_client):
        random_id = get_random_int(999, 10000)
        response = http_client.send_request(
            HttpMethods.DELETE, f"{self.ENDPOINT}/{random_id}"
        )
        assert response.status_code == 404, "Wrong status code"
        assert response.json() == self.ERROR_MESSAGE, "Error message is wrong"

    @allure.title("Delete order wrong data")
    @pytest.mark.parametrize("wrong_data", (1.1, [], "123"))
    def test_delete_order_invalid_data(self, http_client, wrong_data):
        response = http_client.send_request(
            HttpMethods.DELETE, f"{self.ENDPOINT}/{wrong_data}"
        )
        assert response.status_code == 404, "Wrong status code"
        assert response.json() == self.ERROR_MESSAGE, "Error message is wrong"


@allure.suite("Business logic")
class TestBusinessLogic:
    @allure.title("Order status has been changed to executed")
    def test_order_execution(self, http_client, new_order):
        time.sleep(6) # wait until order has been executed
        response = http_client.send_request(HttpMethods.GET, f"/orders/{new_order['id']}")
        assert response.status_code == 200
        assert response.json()['status'] == 'executed'

