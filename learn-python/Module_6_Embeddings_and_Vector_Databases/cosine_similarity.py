# Example: Cosine Similarity
# Demonstrates how to calculate cosine similarity between vectors

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define vectors
vector_a = np.array([[1, 2, 3]])
vector_b = np.array([[4, 5, 6]])

# Calculate cosine similarity
similarity = cosine_similarity(vector_a, vector_b)
print("Cosine Similarity:", similarity[0][0])
