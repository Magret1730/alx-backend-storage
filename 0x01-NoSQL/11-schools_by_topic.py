#!/usr/bin/env python3
""" Task 11 """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    function that returns the list of school having a specific topic

    Args:
    mongo_collection - collection
    topic(string) - topic to use to filter
    """

    topics = mongo_collection.find({"topics": topic})
    return list(topics)
