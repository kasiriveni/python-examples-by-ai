"""
This script demonstrates metadata filtering in vector search using a generic approach.
Topics covered:
1. Adding vectors with metadata.
2. Querying vectors with metadata filters.
"""

class MetadataVectorIndex:
    def __init__(self):
        self.vectors = []

    def add(self, vector, metadata):
        self.vectors.append({"vector": vector, "metadata": metadata})

    def query(self, query_vector, top_k=1, metadata_filter=None):
        results = []
        for item in self.vectors:
            if metadata_filter:
                if not all(item["metadata"].get(k) == v for k, v in metadata_filter.items()):
                    continue
            distance = sum((a - b) ** 2 for a, b in zip(item["vector"], query_vector)) ** 0.5
            results.append((item, distance))
        results.sort(key=lambda x: x[1])
        return results[:top_k]

# Example usage
index = MetadataVectorIndex()

# Add vectors with metadata
index.add([0.1, 0.2, 0.3], {"category": "A", "id": 1})
index.add([0.4, 0.5, 0.6], {"category": "B", "id": 2})
index.add([0.7, 0.8, 0.9], {"category": "A", "id": 3})

# Query with metadata filtering
query_result = index.query([0.15, 0.25, 0.35], top_k=2, metadata_filter={"category": "A"})
print("Query Result:", query_result)
