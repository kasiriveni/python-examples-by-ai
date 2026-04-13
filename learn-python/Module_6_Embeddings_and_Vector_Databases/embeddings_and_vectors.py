"""
Module 6: Embeddings and Vector Databases - concepts and patterns.
"""
import math
import json
from dataclasses import dataclass, field

# === Vector Operations ===
print("=== Vector Operations ===")

class Vector:
    def __init__(self, values):
        self.values = list(values)
        self.dim = len(self.values)

    def dot(self, other):
        return sum(a * b for a, b in zip(self.values, other.values))

    def magnitude(self):
        return math.sqrt(sum(x**2 for x in self.values))

    def cosine_similarity(self, other):
        dot_prod = self.dot(other)
        mag_prod = self.magnitude() * other.magnitude()
        return dot_prod / mag_prod if mag_prod > 0 else 0

    def euclidean_distance(self, other):
        return math.sqrt(sum((a - b)**2 for a, b in zip(self.values, other.values)))

    def normalize(self):
        mag = self.magnitude()
        return Vector([x / mag for x in self.values]) if mag > 0 else self

    def __repr__(self):
        return f"Vector({self.values[:3]}{'...' if self.dim > 3 else ''})"

# Demo
v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])
print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"Cosine similarity: {v1.cosine_similarity(v2):.4f}")
print(f"Euclidean distance: {v1.euclidean_distance(v2):.4f}")
print(f"Dot product: {v1.dot(v2)}")

# === Simple Embedding Simulation ===
print("\n=== Text Embedding (Simulated) ===")

import hashlib

def simple_embed(text, dim=8):
    """Simple deterministic embedding for demonstration."""
    # In production, use OpenAI, sentence-transformers, etc.
    h = hashlib.sha256(text.lower().encode()).hexdigest()
    values = [int(h[i:i+2], 16) / 255.0 for i in range(0, dim * 2, 2)]
    return Vector(values).normalize()

texts = [
    "Python is a programming language",
    "Python is used for web development",
    "Java is a programming language",
    "The weather is sunny today",
]

embeddings = [(text, simple_embed(text)) for text in texts]
print("Similarity matrix:")
for i, (t1, e1) in enumerate(embeddings):
    for j, (t2, e2) in enumerate(embeddings):
        if i < j:
            sim = e1.cosine_similarity(e2)
            print(f"  '{t1[:30]}' vs '{t2[:30]}': {sim:.3f}")

# === In-Memory Vector Store ===
print("\n=== Vector Store ===")

@dataclass
class Document:
    id: str
    text: str
    embedding: Vector = None
    metadata: dict = field(default_factory=dict)

class VectorStore:
    def __init__(self):
        self.documents = {}

    def add(self, doc_id, text, metadata=None):
        embedding = simple_embed(text)
        doc = Document(id=doc_id, text=text, embedding=embedding, metadata=metadata or {})
        self.documents[doc_id] = doc
        return doc

    def search(self, query, top_k=3):
        query_embedding = simple_embed(query)
        results = []
        for doc in self.documents.values():
            similarity = query_embedding.cosine_similarity(doc.embedding)
            results.append((doc, similarity))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def delete(self, doc_id):
        self.documents.pop(doc_id, None)

    def __len__(self):
        return len(self.documents)

# Build and query vector store
store = VectorStore()
store.add("1", "Python web development with Flask", {"topic": "web"})
store.add("2", "Machine learning with scikit-learn", {"topic": "ml"})
store.add("3", "Building REST APIs in Python", {"topic": "api"})
store.add("4", "Data analysis with pandas", {"topic": "data"})
store.add("5", "Deep learning neural networks", {"topic": "ml"})

query = "How to build a web API"
results = store.search(query, top_k=3)
print(f"Query: '{query}'")
for doc, score in results:
    print(f"  [{score:.3f}] {doc.text} ({doc.metadata})")

# === Chunking Strategies ===
print("\n=== Text Chunking ===")

def chunk_by_size(text, chunk_size=100, overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def chunk_by_sentences(text, max_sentences=3):
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = ' '.join(sentences[i:i + max_sentences])
        chunks.append(chunk)
    return chunks

sample_text = "Python is versatile. It supports web development. Machine learning is popular. Data science uses Python extensively. Flask and Django are web frameworks."
chunks = chunk_by_sentences(sample_text, max_sentences=2)
print("Chunks by sentences:")
for i, chunk in enumerate(chunks):
    print(f"  [{i}] {chunk}")
