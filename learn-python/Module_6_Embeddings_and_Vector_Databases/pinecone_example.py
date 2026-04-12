"""
This script demonstrates the use of Pinecone for cloud-based vector database operations.
Topics covered:
1. Index creation and management.
2. Upserting and querying vectors.
"""

import pinecone

# Initialize Pinecone
pinecone.init(api_key="YOUR_API_KEY", environment="us-west1-gcp")

# Create an index
index_name = "example-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=3)

# Connect to the index
index = pinecone.Index(index_name)

# Upsert vectors
vectors = [
    ("vec1", [0.1, 0.2, 0.3]),
    ("vec2", [0.4, 0.5, 0.6]),
    ("vec3", [0.7, 0.8, 0.9])
]
index.upsert(vectors)

# Query the index
query_result = index.query(vector=[0.15, 0.25, 0.35], top_k=2, include_metadata=True)
print("Query Result:", query_result)
