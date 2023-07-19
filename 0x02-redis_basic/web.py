#!/usr/bin/env python3
""" Redis with requests """
import requests
from functools import wraps
from typing import Callable
import redis

def count(method: Callable) -> Callable:
    """ Count the call to requests """
    r = redis.Redis()

    @wraps(method)
    def wrapped(url: str) -> str:
        """ function that will count """
        count_key = f"count:{url}"
        cached_key = f"cached:{url}"
        
        r.incr(count_key)
        expiration_count = r.get(cached_key)

        if expiration_count:
            return expiration_count.decode('utf-8')

        html = method(url)
        r.setex(cached_key, 10, html)

        return html

    return wrapped

@count
def get_page(url: str) -> str:
    """ module to obtain the HTML """
    return requests.get(url).text

