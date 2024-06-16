#!/usr/bin/env python3
""" TAsk 9 """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    function that inserts a new document in a collection based on kwargs

    Args:
    mongo_collection - pymongo collection object
    **kwargs - fields for the new document

    Returns:
    new _id
    """
    new_document = mongo_collection.insert_one(kwargs)

    return mongo_collection.inserted_id
