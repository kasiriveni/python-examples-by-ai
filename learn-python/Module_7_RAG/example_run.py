"""Example runner for Module 7: RAG (simple text chunker)"""


def chunk_text(text, chunk_size=50):
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


def main():
    print("Module 7 - RAG example")
    t = """
    This is a short example document. It will be split into small chunks
    to simulate how a retrieval pipeline might chunk documents for indexing.
    """
    chunks = list(chunk_text(t.strip(), chunk_size=40))
    for i, c in enumerate(chunks, 1):
        print(f"Chunk {i}:", repr(c))


if __name__ == "__main__":
    main()
