# Example: Document Loader for RAG
# Demonstrates how to load and split documents for RAG pipelines

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load a PDF document
loader = PyPDFLoader("example.pdf")
documents = loader.load()

# Split the document into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

print(f"Number of chunks: {len(chunks)}")
