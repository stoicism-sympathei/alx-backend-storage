#!/usr/bin/env python3
""" Redis with requests """

import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def count_url_access(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cached_key = f"cached:{url}"

        response = redis_client.incr(count_key)
        if response == 1:
            redis_client.expire(count_key, 10)

        cached_result = redis_client.get(cached_key)
        if cached_result:
            return cached_result.decode()

        html_content = method(url)
        redis_client.setex(cached_key, 10, html_content)

        return html_content

    return wrapper

@count_url_access
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

