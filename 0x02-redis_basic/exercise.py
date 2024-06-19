#!/usr/bin/env python3
""" Task 0 """
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
        self._redis = redis.Redis()
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

        # Debug print statement
        # print(f"Generated key: {random_key}")
        # Store the data in Redis with the generated key
        try:
            self._redis.set(random_key, data)
            # Verify that the data was stored
            stored_data = self._redis.get(random_key)
            # print(f"Attempted to store data: {data}")
            # print(f"Stored data: {stored_data}")
        except Exception as e:
            print(f"Error storing data: {e}")

        return random_key
