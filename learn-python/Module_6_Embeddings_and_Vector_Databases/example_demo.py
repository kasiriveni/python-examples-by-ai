"""Embeddings demo: nearest neighbor by brute-force (pure Python)"""
import math


def l2(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def nearest(query, vectors):
    return min(vectors, key=lambda v: l2(query, v))


def main():
    vecs = [[1, 0], [0, 1], [1, 1]]
    q = [0.9, 0.1]
    print("Nearest to", q, "is", nearest(q, vecs))


if __name__ == '__main__':
    main()
