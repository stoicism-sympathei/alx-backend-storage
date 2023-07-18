#!/usr/bin/env python3
""" Log Stats module. """
from pymongo import MongoClient

def get_top_ips(mongo_collection, limit=10):
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]

    top_ips = list(mongo_collection.aggregate(pipeline))
    return top_ips

if __name__ == "__main__":
    client = MongoClient(host="localhost", port=27017)
    db = client.logs

    # Get the total number of logs
    total_logs = db.nginx.count_documents({})

    # Get the number of logs per method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    methods_count = {method: db.nginx.count_documents({"method": method}) for method in methods}

    # Get the number of status checks
    status_checks = db.nginx.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")

    print(f"{status_checks} status check")

    # Get the top 10 IPs
    top_ips = get_top_ips(db.nginx)
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

