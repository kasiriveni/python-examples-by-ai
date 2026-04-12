# Example: RAG Pipeline
# Demonstrates a full RAG pipeline with LangChain

from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Create FAISS vector store
embeddings = OpenAIEmbeddings()
faiss_store = FAISS(embeddings)
faiss_store.add_texts(["Hello World", "AI Engineer", "LangChain is great"])

# Create RAG pipeline
retriever = faiss_store.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm="openai", retriever=retriever)

# Query the pipeline
query = "What is LangChain?"
response = qa_chain.run(query)
print("Response:", response)
