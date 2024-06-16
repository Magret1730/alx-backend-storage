#!/usr/bin/env python3
""" Task 11 """
from pymongo import MongoClient


def log_stats():
    """
    Function that provides some stats about Nginx logs stored in MongoDB.
    """

    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})

    # Count for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method})
                     for method in methods}

    # Count for GET requests to the path/status
    status_check = collection\
        .count_documents({"method": "GET", "path": "/status"})

    # Aggregate pipeline to get top 10 IPs by count
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    # Execute aggregation pipeline
    top_ips = list(collection.aggregate(pipeline))

    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
