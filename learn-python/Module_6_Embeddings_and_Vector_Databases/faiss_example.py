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