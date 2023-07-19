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
        response = redis_client.incr(count_key)
        if response == 1:
            # Set expiration time for the count_key only when it's newly created
            redis_client.expire(count_key, 10)

        # Check if the result is already cached
        cached_result = redis_client.get(cached_key)
        if cached_result:
            return cached_result.decode()

        # Fetch the HTML content using requests
        html_content = method(url)

        # Cache the HTML content with an expiration time of 10 seconds
        redis_client.setex(cached_key, 10, html_content)

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

