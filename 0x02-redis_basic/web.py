#!/usr/bin/env python3
""" Redis with requests """

import requests
import redis
from functools import wraps
from typing import Callable

# Connect to the Redis server
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def count_url_access(method: Callable) -> Callable:
    """
    Decorator to track the number of times a particular URL is accessed.
    Increments a counter for each URL and sets its expiration time to 10 seconds.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cached_key = f"cached:{url}"

        # Increment the URL access count
        count = redis_client.incr(count_key)

        # Fetch the current count
        if count == 1:
            # Fetch the HTML content using requests if it's the first access
            html_content = method(url)

            # Cache the HTML content with an expiration time of 10 seconds
            redis_client.setex(cached_key, 10, html_content)
        else:
            # Get the cached HTML content
            html_content = redis_client.get(cached_key).decode()

        return html_content

    return wrapper

@count_url_access
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
