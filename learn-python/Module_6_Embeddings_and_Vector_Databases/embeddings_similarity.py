"""
This script demonstrates the concept of embeddings and similarity metrics.
Topics covered:
1. Generating embeddings using a pre-trained model.
2. Calculating cosine similarity, dot product, and Euclidean distance.
"""

from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import numpy as np

# Example embeddings (e.g., from a model like text-embedding-ada-002)
embedding_1 = np.array([0.1, 0.2, 0.3])
embedding_2 = np.array([0.2, 0.1, 0.4])

# Cosine Similarity
cos_sim = cosine_similarity([embedding_1], [embedding_2])[0][0]
print(f"Cosine Similarity: {cos_sim}")

# Dot Product
dot_prod = np.dot(embedding_1, embedding_2)
print(f"Dot Product: {dot_prod}")

# Euclidean Distance
euc_dist = euclidean(embedding_1, embedding_2)
print(f"Euclidean Distance: {euc_dist}")
