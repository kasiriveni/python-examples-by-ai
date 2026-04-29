"""Example runner for Module 6: Embeddings & Vector DBs (pure-Python demo)"""
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def main():
    print("Module 6 - Embeddings example")
    v1 = [1, 0, 1]
    v2 = [0.5, 0.5, 0]
    print("v1", v1)
    print("v2", v2)
    print("Cosine similarity:", cosine(v1, v2))


if __name__ == "__main__":
    main()
