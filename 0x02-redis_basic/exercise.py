#!/usr/bin/env python3
"""Module declares a redis class and methods"""
import redis
import uuid
from typing import Union, Optional, Callable


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
