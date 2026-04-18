# Core Python Concepts

## Core Themes
- Retrieval-augmented generation pipeline design.
- Document loading, splitting, indexing, and retrieval.
- Hybrid retrieval and RAG evaluation strategies.

## Core Theme Examples
- Example 1: Loading PDFs and splitting documents into chunks.
- Example 2: Hybrid retrieval combining FAISS dense and BM25 sparse search.
- Example 3: Evaluating RAG faithfulness and answer relevance scores.

## Files and Concepts
- document_loader.py: document ingestion, PDF loading, preprocessing
- document_loader_example.py: PyPDFLoader, recursive text splitting
- evaluate_rag.py: relevance, faithfulness, and answer-quality evaluation
- hybrid_retrieval.py: dense retrieval with FAISS, sparse retrieval with BM25, hybrid fusion
- rag_architecture.py: RAG architecture stages and system flow
- rag_pipeline.py: RetrievalQA-style chaining and full pipeline assembly
- text_splitter.py: chunk size, overlap, and splitting strategies

## Core Example
This example stores text chunks and retrieves the ones matching a query word.

```python
chunks = [
	"Python uses functions and classes.",
	"RAG systems retrieve documents before answering.",
]

query = "retrieve"
matches = [chunk for chunk in chunks if query in chunk.lower()]

print(matches)
```
