"""
This script demonstrates various chunking strategies for text data.
Topics covered:
1. Fixed-size chunking.
2. Sentence-based chunking.
3. Semantic chunking.
4. Recursive chunking.
"""

from nltk.tokenize import sent_tokenize

# Example text
document = """
Natural language processing (NLP) is a subfield of artificial intelligence (AI).
It focuses on the interaction between computers and humans through natural language.
Applications include machine translation, sentiment analysis, and chatbots.
"""

# Fixed-size chunking
def fixed_size_chunking(text, chunk_size):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Sentence-based chunking
def sentence_based_chunking(text):
    return sent_tokenize(text)

# Semantic chunking (placeholder for actual semantic logic)
def semantic_chunking(text):
    # Example: Split by keywords (simplified)
    return text.split("AI")

# Recursive chunking (placeholder for recursive logic)
def recursive_chunking(text, max_length):
    if len(text) <= max_length:
        return [text]
    mid = len(text) // 2
    return recursive_chunking(text[:mid], max_length) + recursive_chunking(text[mid:], max_length)

# Demonstrate chunking strategies
print("Fixed-size Chunking:", fixed_size_chunking(document, 10))
print("Sentence-based Chunking:", sentence_based_chunking(document))
print("Semantic Chunking:", semantic_chunking(document))
print("Recursive Chunking:", recursive_chunking(document, 50))
