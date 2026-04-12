# Example: Hybrid Retrieval for RAG
# Demonstrates dense and sparse retrieval for RAG pipelines

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever

# Dense retrieval with FAISS
embeddings = OpenAIEmbeddings()
faiss_store = FAISS(embeddings)
faiss_store.add_texts(["Hello World", "AI Engineer", "LangChain is great"])

# Sparse retrieval with BM25
bm25_retriever = BM25Retriever()
bm25_retriever.add_texts(["Hello World", "AI Engineer", "LangChain is great"])

# Hybrid retrieval
query = "AI"
dense_results = faiss_store.similarity_search(query)
sparse_results = bm25_retriever.get_relevant_documents(query)

print("Dense Results:", dense_results)
print("Sparse Results:", sparse_results)
