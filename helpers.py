from random import randint, choices

import json
import re

from logging import getLogger

logger = getLogger(__name__)


def get_stock_name() -> list[str]:
    stocks = ("EUR", "USD", "GEL", "AED")
    return choices(stocks, k=2)


def get_random_int(start: int, stop: int) -> int:
    return randint(999, 9999)


def create_order_data() -> dict[str, int | str]:
    return {"stocks": "".join(get_stock_name()), "quantity": randint(0, 100)}


def extract_dict_from_string(target) -> dict:
    match = re.search(r"\{.*?\}", target)
    if match:
        json_str = match.group(0)
        try:
            parsed_dict = json.loads(json_str)
            return parsed_dict
        except json.JSONDecodeError as e:
            logger.info(f"Error parsing JSON: {e}")
    else:
        logger.info("No JSON dictionary found in string")
