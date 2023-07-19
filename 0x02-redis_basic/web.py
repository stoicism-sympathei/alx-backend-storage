#!/usr/bin/env python3
""" Redis with requests """

import redis
import requests
from functools import wraps
from typing import Callable

# Connect to the Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def track_url_access_count(func: Callable) -> Callable:
    """
    Decorator to track the number of times a particular URL is accessed.
    Increments a counter for each URL and sets its expiration time to 10 seconds.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        count = redis_client.incr(count_key)
        redis_client.expire(count_key, 10)  # Set expiration time to 10 seconds
        print(f"Accessed {url} {count} time(s)")
        return func(url)
    return wrapper

@track_url_access_count
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL using the requests module.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

