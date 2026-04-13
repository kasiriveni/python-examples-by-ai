"""
Machine Learning and AI: Clustering algorithms from scratch.
"""
import math
import random
from dataclasses import dataclass, field
from typing import Iterator

# ═══════════════════════════════════════════
# 1. K-Means clustering
# ═══════════════════════════════════════════
Point = tuple[float, ...]

def euclidean(a: Point, b: Point) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def centroid(points: list[Point]) -> Point:
    n = len(points)
    return tuple(sum(p[i] for p in points) / n for i in range(len(points[0])))

class KMeans:
    """K-Means clustering (Lloyd's algorithm)."""

    def __init__(self, k: int, max_iter: int = 100, tol: float = 1e-4, seed: int = 42):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.seed = seed
        self.centroids_: list[Point] = []
        self.labels_: list[int] = []
        self.inertia_: float = 0.0
        self.n_iter_: int = 0

    def fit(self, X: list[Point]) -> "KMeans":
        rng = random.Random(self.seed)
        # K-Means++ initialization
        self.centroids_ = self._kmeanspp_init(X, rng)

        for iteration in range(self.max_iter):
            # Assignment step
            labels = [self._nearest(x) for x in X]

            # Update step
            new_centroids = []
            for k in range(self.k):
                cluster_points = [X[i] for i, lbl in enumerate(labels) if lbl == k]
                if cluster_points:
                    new_centroids.append(centroid(cluster_points))
                else:
                    new_centroids.append(self.centroids_[k])  # keep if empty

            # Convergence check
            shift = max(euclidean(self.centroids_[k], new_centroids[k]) for k in range(self.k))
            self.centroids_ = new_centroids
            self.labels_ = labels
            self.n_iter_ = iteration + 1
            if shift < self.tol:
                break

        # Compute inertia (within-cluster sum of squares)
        self.inertia_ = sum(
            euclidean(X[i], self.centroids_[lbl]) ** 2
            for i, lbl in enumerate(self.labels_)
        )
        return self

    def _kmeanspp_init(self, X: list[Point], rng: random.Random) -> list[Point]:
        centers = [rng.choice(X)]
        for _ in range(self.k - 1):
            dists = [min(euclidean(x, c) ** 2 for c in centers) for x in X]
            total = sum(dists)
            probs = [d / total for d in dists]
            # Weighted random choice
            r = rng.random()
            cumulative = 0.0
            for i, p in enumerate(probs):
                cumulative += p
                if r <= cumulative:
                    centers.append(X[i]); break
            else:
                centers.append(X[-1])
        return centers

    def _nearest(self, x: Point) -> int:
        return min(range(self.k), key=lambda k: euclidean(x, self.centroids_[k]))

    def predict(self, X: list[Point]) -> list[int]:
        return [self._nearest(x) for x in X]

# ═══════════════════════════════════════════
# 2. DBSCAN clustering
# ═══════════════════════════════════════════
NOISE = -1

class DBSCAN:
    """Density-Based Spatial Clustering (no need to specify k)."""

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels_: list[int] = []
        self.n_clusters_: int = 0

    def fit(self, X: list[Point]) -> "DBSCAN":
        n = len(X)
        self.labels_ = [-2] * n   # -2 = unvisited
        cluster_id = 0

        for i in range(n):
            if self.labels_[i] != -2:
                continue
            neighbors = self._range_query(X, i)
            if len(neighbors) < self.min_samples:
                self.labels_[i] = NOISE
                continue
            cluster_id += 1
            self.labels_[i] = cluster_id
            seed_set = list(neighbors)
            j = 0
            while j < len(seed_set):
                q = seed_set[j]; j += 1
                if self.labels_[q] == NOISE:
                    self.labels_[q] = cluster_id
                if self.labels_[q] != -2:
                    continue
                self.labels_[q] = cluster_id
                q_neighbors = self._range_query(X, q)
                if len(q_neighbors) >= self.min_samples:
                    # Extend seed set with new undiscovered points
                    for nb in q_neighbors:
                        if self.labels_[nb] == -2:
                            seed_set.append(nb)

        self.n_clusters_ = cluster_id
        return self

    def _range_query(self, X: list[Point], idx: int) -> list[int]:
        return [i for i, x in enumerate(X) if euclidean(x, X[idx]) <= self.eps]

# ═══════════════════════════════════════════
# 3. Metrics
# ═══════════════════════════════════════════
def silhouette_score(X: list[Point], labels: list[int]) -> float:
    """Silhouette score: how separated clusters are. Range [-1, 1]."""
    n = len(X)
    unique = set(labels) - {NOISE}
    if len(unique) < 2:
        return 0.0
    scores = []
    for i in range(n):
        if labels[i] == NOISE:
            continue
        same = [X[j] for j in range(n) if j != i and labels[j] == labels[i]]
        a = sum(euclidean(X[i], s) for s in same) / len(same) if same else 0.0
        b_candidates = []
        for lbl in unique:
            if lbl == labels[i]:
                continue
            other = [X[j] for j in range(n) if labels[j] == lbl]
            if other:
                b_candidates.append(sum(euclidean(X[i], o) for o in other) / len(other))
        b = min(b_candidates) if b_candidates else 0.0
        s = (b - a) / max(a, b) if max(a, b) > 0 else 0.0
        scores.append(s)
    return sum(scores) / len(scores) if scores else 0.0

# ═══════════════════════════════════════════
# 4. Generate synthetic datasets
# ═══════════════════════════════════════════
def make_blobs(n_samples: int, centers: list[Point], std: float = 0.5,
               seed: int = 42) -> tuple[list[Point], list[int]]:
    rng = random.Random(seed)
    X, y = [], []
    per_center = n_samples // len(centers)
    for lbl, center in enumerate(centers):
        for _ in range(per_center):
            point = tuple(c + rng.gauss(0, std) for c in center)
            X.append(point); y.append(lbl)
    return X, y

def make_circles(n_samples: int = 100, noise: float = 0.05, seed: int = 42) -> tuple[list[Point], list[int]]:
    rng = random.Random(seed)
    X, y = [], []
    for i in range(n_samples):
        lbl = i % 2
        r = 0.5 if lbl == 0 else 1.0
        angle = rng.uniform(0, 2 * math.pi)
        x = r * math.cos(angle) + rng.gauss(0, noise)
        yv = r * math.sin(angle) + rng.gauss(0, noise)
        X.append((x, yv)); y.append(lbl)
    return X, y

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    centers = [(0.0, 0.0), (5.0, 0.0), (2.5, 4.0)]
    X, y_true = make_blobs(150, centers, std=0.6)

    print("=== K-Means ===")
    km = KMeans(k=3, seed=0)
    km.fit(X)
    print(f"  Converged in {km.n_iter_} iterations")
    print(f"  Inertia: {km.inertia_:.2f}")
    for i, c in enumerate(km.centroids_):
        print(f"  Centroid {i}: ({c[0]:.2f}, {c[1]:.2f})")
    # Simple accuracy check
    from collections import Counter
    label_map = {}
    for pred, true in zip(km.labels_, y_true):
        label_map.setdefault(pred, Counter())[true] += 1
    correct = sum(c.most_common(1)[0][1] for c in label_map.values())
    print(f"  Accuracy (cluster-mapped): {correct / len(y_true):.1%}")

    sil = silhouette_score(X, km.labels_)
    print(f"  Silhouette score: {sil:.3f}")

    print("\n=== DBSCAN ===")
    X_circles, y_circles = make_circles(120, noise=0.03)
    db = DBSCAN(eps=0.3, min_samples=4)
    db.fit(X_circles)
    print(f"  Clusters found: {db.n_clusters_}")
    noise_count = db.labels_.count(NOISE)
    print(f"  Noise points: {noise_count}")
    cluster_sizes = Counter(l for l in db.labels_ if l != NOISE)
    for cid, size in sorted(cluster_sizes.items()):
        print(f"  Cluster {cid}: {size} points")

    print("\n=== K-Means Elbow Method ===")
    inertias = []
    for k in range(1, 7):
        km_k = KMeans(k=k, seed=0)
        km_k.fit(X)
        inertias.append(km_k.inertia_)
        print(f"  k={k}: inertia={km_k.inertia_:.1f}")
    print("  (Elbow typically at k=3 for this dataset)")
