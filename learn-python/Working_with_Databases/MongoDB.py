# MongoDB: NoSQL Database

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["exampledb"]
collection = db["users"]

# Insert a document
collection.insert_one({"name": "Alice", "age": 30})

# Query documents
for user in collection.find():
    print(user)
