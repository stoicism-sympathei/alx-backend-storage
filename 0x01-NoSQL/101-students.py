#!/usr/bin/env python3

from pymongo import MongoClient

def top_students(mongo_collection):
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

