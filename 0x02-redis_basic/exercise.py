#!/usr/bin/env python3
""" Exercise module. """
from typing import Callable, Optional, Union
from functools import wraps
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """ count_calls decorator. """
    @wraps(method)
    def count_calls_wrapper(self, *args, **kwargs) -> bytes:
        """ count_calls wrapper. """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return count_calls_wrapper


def call_history(method: Callable) -> Callable:
    """ call_history decorator. """
    inputs = f"{method.__qualname__}:inputs"
    outputs = f"{method.__qualname__}:outputs"

    @wraps(method)
    def call_history_wrapper(self, *args, **kwargs) -> bytes:
        """ call_history wrapper. """
        self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs, output)

        return output

    return call_history_wrapper


def replay(method: Callable):
    """ Replay the calls of a specific method """
    m_name = method.__qualname__
    inputs = f"{m_name}:inputs"
    outputs = f"{m_name}:outputs"
    r = redis.Redis()

    data = r.get(m_name).decode("utf-8")
    inputs_list = r.lrange(inputs, 0, -1)
    outputs_list = r.lrange(outputs, 0, -1)

    print(f"{m_name} was called {data} times:")

    for k, v in zip(inputs_list, outputs_list):
        print(f"{m_name}(*{k.decode('utf-8')}) -> {v.decode('utf-8')}")


class Cache:
    """ Class for methods that operate a caching system """

    def __init__(self):
        """ Instance of Redis db """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self,
              data: UnionOfTypes) -> str:
        """
        Method takes a data argument and returns a string
        Generate a random key (e.g. using uuid), store the input data in Redis
        using the random key and return the key
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data stored at a key
        converts the data back to the desired format
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, data: str) -> str:
        """ get a string """
        return self.get(key, str)

    def get_int(self, data: str) -> int:
        """ get an int """
        return self.get(key, int)
