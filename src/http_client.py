import json
from enum import Enum
import allure
import requests
from logging import getLogger

logger = getLogger(__name__)


class HttpMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpClient:
    def __init__(self, url):
        self.base_url = url

    def send_request(self, method: HttpMethods, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"

        if kwargs:
            if "data" in kwargs and isinstance(kwargs["data"], dict):
                kwargs["data"] = json.dumps(kwargs["data"])

        try:
            with allure.step(f"Send request {method} on {url}"):
                response = requests.request(method, url, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request {method} couldn't be send to {url}. Error {e}")
        else:
            logger.info(
                f"Request {method} has been sent to {url}. "
                f"Requests data - {response.request.body}. "
                f"Response status code - {response.status_code}. "
                f"Response - {response.text}. "
                f"Response headers - {response.headers}."
            )
            return response
