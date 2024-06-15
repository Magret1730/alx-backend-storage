#!/usr/bin/env python3
""" Task 8 """
import pymongo


def list_all(mongo_collection):
    """
    Python function that lists all documents in a collection

    Arg:
    mongo_collection: a collection

    Return:
    A list of the collection or
    empty list if no collectio
    """

    # Find all documents
    documents = mongo_collection.find({})

    # Convert documents to a list (if collection is empty,
    # it will be an empty list)
    return list(documents)
