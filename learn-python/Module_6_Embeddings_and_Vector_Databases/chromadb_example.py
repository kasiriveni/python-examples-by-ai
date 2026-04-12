# Example: ChromaDB for Vector Search
# Demonstrates how to use ChromaDB for managing embeddings

from chromadb.config import Settings
from chromadb.client import Client

# Initialize ChromaDB client
client = Client(Settings())

# Create a collection
collection = client.create_collection(name="example_collection")

# Add embeddings
data = [
    {"id": "1", "embedding": [0.1, 0.2, 0.3], "metadata": {"text": "Hello World"}},
    {"id": "2", "embedding": [0.4, 0.5, 0.6], "metadata": {"text": "AI Engineer"}}
]
collection.add(data)

# Query the collection
results = collection.query(embedding=[0.1, 0.2, 0.3], k=1)
print("Query Results:", results)

"""
This script demonstrates the use of ChromaDB for lightweight vector database operations.
Topics covered:
1. Adding vectors to a collection.
2. Querying vectors with metadata filtering.
"""

# Add vectors with metadata
collection.add(
    embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
    metadatas=[{"id": 1, "category": "A"}, {"id": 2, "category": "B"}, {"id": 3, "category": "A"}],
    ids=["vec1", "vec2", "vec3"]
)

# Query the collection
query_result = collection.query(
    query_embeddings=[[0.15, 0.25, 0.35]],
    n_results=2,
    where={"category": "A"}  # Metadata filtering
)

print("Query Result:", query_result)
