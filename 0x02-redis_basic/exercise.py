#!/usr/bin/env python3
"""Module declares a redis class and methods"""
import random
import redis
import uuid
from typing import Union


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
        self._redis.flushdb  # Flush the Redis database

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
