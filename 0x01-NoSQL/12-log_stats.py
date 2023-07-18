#!/usr/bin/env python3

"""
Script to provide some stats about Nginx logs stored in MongoDB.

Database: logs
Collection: nginx

Output format (same as the example):
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with the method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
    one line with the number of documents with:
        method=GET
        path=/status
"""

import pymongo

def get_nginx_logs_stats():
    """
    Connects to MongoDB and fetches the required statistics.

    Returns:
        total_logs (int): Total number of logs in the collection.
        method_counts (dict): Dictionary containing counts of each method.
        status_check_count (int): Number of logs with method=GET and path=/status.
    """
    # MongoDB connection details
    host = 'localhost'
    port = 27017
    database_name = 'logs'
    collection_name = 'nginx'

    # Connect to MongoDB
    client = pymongo.MongoClient(host, port)
    db = client[database_name]
    collection = db[collection_name]

    # Get the number of logs
    total_logs = collection.count_documents({})

    # Get the number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Get the number of logs with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Close the MongoDB connection
    client.close()

    return total_logs, method_counts, status_check_count

def main():
    """
    Main function to fetch and display Nginx logs stats.
    """
    total_logs, method_counts, status_check_count = get_nginx_logs_stats()

    # Print the stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}:", count)
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    main()

