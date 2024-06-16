#!/usr/bin/env python3
"""
def top_students(mongo_collection):

    function that returns all students sorted by average score
    scores = mongo_collection.get("score": [])
    if scores:
        average_score = sum(scores) / len(scores)
    mongo_collection.update({"name": "name"},
    {"$push": {"averageScore": average_score}})
    return mongo_collection.find({"name": "name"})
    .sort({"averageScore": average_score}, {"name": 1, "averageScore": 1})
"""

import pymongo


def top_students(mongo_collection):
    """
    Function that returns all students sorted by average score.
    """
    # Aggregation pipeline to calculate average score
    pipeline = [
        {
            "$unwind": "$topics"
            # Unwind the topics array to work with individual topics
        },
        {
            "$group": {
                "_id": "$name",
                "averageScore": {"$avg": "$topics.score"}
                # Calculate average score for each student
            }
        },
        {
            "$project": {
                "_id": 0,  # Exclude _id field from final result
                "name": "$_id",  # Rename _id as name
                "averageScore": 1  # Include averageScore in final result
            }
        },
        {
            "$sort": {"averageScore": -1}  # Sort by averageScore descending
        }
    ]

    # Aggregate pipeline to compute average scores
    average_scores = list(mongo_collection.aggregate(pipeline))

    # Update each student document with their calculated average score
    for student in average_scores:
        mongo_collection.update_one(
            {"name": student["name"]},
            {"$set": {"averageScore": student["averageScore"]}}
        )

    # Return all students sorted by averageScore
    return mongo_collection.find().sort("averageScore", pymongo.DESCENDING)
