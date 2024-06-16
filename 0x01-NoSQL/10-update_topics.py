#!/usr/bin/env python3
""" Task 10 """
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    function that changes all topics of a school document based on the name

    Args:
    mongo_collection - collection
    name - document to change
    topics - document to change to
    """

    updated = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
