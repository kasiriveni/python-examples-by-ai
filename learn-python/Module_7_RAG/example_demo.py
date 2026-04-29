"""RAG demo: keyword-based retrieval from chunks"""


def retrieve(query, chunks):
    q = query.lower()
    return [c for c in chunks if q in c.lower()]


def main():
    chunks = [
        "Python is a great language for data.",
        "Retrieval augmented generation uses indexed chunks.",
        "Use embeddings to match vectors."
    ]
    print("Query 'retrieval':", retrieve("retrieval", chunks))


if __name__ == '__main__':
    main()
