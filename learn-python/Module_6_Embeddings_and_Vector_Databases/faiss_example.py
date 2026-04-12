# Example: FAISS for Vector Search
# Demonstrates how to use FAISS for similarity search

import faiss
import numpy as np

# Create a dataset of vectors
data = np.random.random((100, 128)).astype('float32')

# Build the FAISS index
index = faiss.IndexFlatL2(128)
index.add(data)

# Query the index
query = np.random.random((1, 128)).astype('float32')
distances, indices = index.search(query, k=5)

print("Nearest neighbors:", indices)

"""
This script demonstrates the use of FAISS for local vector search.
Topics covered:
1. Indexing vectors.
2. Searching for nearest neighbors.
"""

# Create a FAISS index
vector_dimension = 3  # Dimension of the vectors
index = faiss.IndexFlatL2(vector_dimension)

# Add vectors to the index
vectors = np.array([
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9]
], dtype='float32')
index.add(vectors)

# Query the index
query_vector = np.array([[0.15, 0.25, 0.35]], dtype='float32')
k = 2  # Number of nearest neighbors to retrieve
distances, indices = index.search(query_vector, k)

print("Query Vector:", query_vector)
print("Nearest Neighbors (indices):", indices)
print("Distances:", distances)
