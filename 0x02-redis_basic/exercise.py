#!/usr/bin/env python3
"""Module contains exercises on Redis"""
from redis import Redis
from uuid import uuid4
from typing import Callable, Union, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts number of function calls"""
    key = method.__qualname__

    @wraps(method)
    def count(self, *args, **kwargs):
        """count wrapper"""
        self._redis.incr(key, amount=1)
        return method(self, *args, **kwargs)
    return count


def call_history(method: Callable) -> Callable:
    """Stores history of inputs and outputs"""
    @wraps(method)
    def call(self, *args, **kwargs):
        """Wrapper for history"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))

        # return output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output

    return call


class Cache:
    """Models a Cache storage"""

    def __init__(self):
        """class constructor"""
        self._redis = Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores key-value in redis database"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get_int(self, key: str) -> int:
        """returns value as int"""
        data = self._redis.get(key)
        return int.from_bytes(data)

    def get_str(self, key: str) -> str:
        """returns value as key"""
        data = self._redis.get(key)
        return data.decode('utf-8')

    def get(self, key, fn: Callable = None) -> Any:
        """Converts data to desired format"""
        if not fn:
            return self._redis.get(key)
        return fn(self._redis.get(key))


def replay(func):
    redis = Redis()
    fn_name = func.__qualname__
    c = redis.get(fn_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(fn_name, c))
    inputs = redis.lrange("{}:inputs".format(fn_name), 0, -1)
    outputs = redis.lrange("{}:outputs".format(fn_name), 0, -1)
    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*{}) -> {}".format(fn_name, input, output))
