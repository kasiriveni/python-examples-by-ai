"""
This script demonstrates indexing, upserting, and querying vectors using a generic approach.
Topics covered:
1. Indexing vectors.
2. Upserting new vectors.
3. Querying vectors for nearest neighbors.
"""

import numpy as np

class SimpleVectorIndex:
    def __init__(self, dimension):
        self.dimension = dimension
        self.vectors = {}

    def upsert(self, id, vector):
        if len(vector) != self.dimension:
            raise ValueError("Vector dimension mismatch.")
        self.vectors[id] = vector

    def query(self, query_vector, top_k=1):
        if len(query_vector) != self.dimension:
            raise ValueError("Query vector dimension mismatch.")
        distances = {
            id: np.linalg.norm(np.array(vector) - np.array(query_vector))
            for id, vector in self.vectors.items()
        }
        return sorted(distances.items(), key=lambda x: x[1])[:top_k]

# Example usage
index = SimpleVectorIndex(dimension=3)

# Indexing vectors
index.upsert("vec1", [0.1, 0.2, 0.3])
index.upsert("vec2", [0.4, 0.5, 0.6])
index.upsert("vec3", [0.7, 0.8, 0.9])

# Querying vectors
query_result = index.query([0.15, 0.25, 0.35], top_k=2)
print("Query Result:", query_result)
