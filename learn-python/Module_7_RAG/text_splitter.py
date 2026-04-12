# Example: Text Splitter for RAG
# Demonstrates how to split text into chunks for RAG pipelines

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Example text
document = """
LangChain is a framework for developing applications powered by language models.
It enables developers to chain together different components to create complex applications.
"""

# Split the text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
chunks = splitter.split_text(document)

print("Chunks:")
for chunk in chunks:
    print(chunk)
