#!/usr/bin/env python3
"""Module declares a redis class and methods"""
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def call_history(method: Callable) -> Callable:
    """
    Decorator to store history of inputs and outputs of a function in Redis.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Construct keys for inputs and outputs lists
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"
        # Store input arguments as a string in Redis inputs list
        self._redis.rpush(key_inputs, str(args))
        # Execute the original method to get the output
        output = method(self, *args, **kwargs)
        # Store the output in Redis outputs list
        self._redis.rpush(key_outputs, output)
        # Return the original output
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Construct the key using the method's qualified name
        key = f"{method.__qualname__}"
        # print(key)
        # Increment the counter in Redis
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache class
    """
    def __init__(self):
        """
        Initialize the Redis client and store it as a private variable
        Also flush the Redis database
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.
        Returns:
            str: The generated random key.
        """
        random_key = str(uuid.uuid4())  # Generate a random key using uuid4
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, int, float, bytes]:
        """
        Retrieve data from Redis using the given key and an optional Callable
        for conversion.
        Args:
            key (str): The key to retrieve from Redis.
            fn (Optional[Callable]): A callable to convert the data back to
            the desired format.
        Returns:
            Union[str, bytes, int, float, None]: The data retrieved from
            Redis, optionally converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis using the given key.
        Args:
            key (str): The key to retrieve from Redis.
        Returns:
            Optional[str]: The data retrieved from Redis,
            converted to a string.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis using the given key.
        Args:
            key (str): The key to retrieve from Redis.
        Returns:
            Optional[int]: The data retrieved from Redis,
            converted to an integer.
        """
        return self.get(key, fn=int)
