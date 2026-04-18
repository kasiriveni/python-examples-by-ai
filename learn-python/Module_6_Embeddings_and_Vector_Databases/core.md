# Core Python Concepts

## Core Themes
- Embedding vectors and similarity calculations.
- Chunking, indexing, upserts, and vector retrieval.
- Working with FAISS, ChromaDB, Pinecone, and metadata filters.

## Core Theme Examples
- Example 1: Computing cosine similarity between embedding vectors.
- Example 2: Semantic and fixed-size document chunking strategies.
- Example 3: FAISS indexing and nearest-neighbor similarity search.

## Files and Concepts
- chromadb_example.py: ChromaDB collections, metadata-aware storage
- chunking_strategies.py: fixed-size, semantic, recursive, and sentence-based chunking
- cosine_similarity.py: pairwise cosine similarity and vector-distance comparison
- embeddings_and_vectors.py: vector math, magnitudes, dot products, normalization
- embeddings_similarity.py: embedding generation and similarity scoring
- faiss_example.py: FAISS indexing and nearest-neighbor lookup
- indexing_upserting_querying.py: vector indexes, upsert operations, querying flows
- metadata_filtering.py: metadata fields, filter-based retrieval
- pinecone_example.py: Pinecone index creation, upsert, query patterns

## Core Example
This example computes cosine similarity with plain Python lists.

```python
from math import sqrt

def cosine_similarity(left, right):
	dot = sum(a * b for a, b in zip(left, right))
	left_norm = sqrt(sum(value * value for value in left))
	right_norm = sqrt(sum(value * value for value in right))
	return dot / (left_norm * right_norm)

print(round(cosine_similarity([1, 2], [2, 4]), 2))
```
