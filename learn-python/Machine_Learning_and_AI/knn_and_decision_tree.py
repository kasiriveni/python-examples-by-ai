"""
Machine Learning and AI: K-Nearest Neighbors and Decision Tree from scratch.
"""
import math
import random
from collections import Counter

# ═══════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════
def euclidean(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y)**2 for x, y in zip(a, b)))

def accuracy(y_true, y_pred) -> float:
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)

def train_test_split(X, y, test_size=0.25, seed=42):
    data = list(zip(X, y))
    random.seed(seed)
    random.shuffle(data)
    split = int(len(data) * (1 - test_size))
    train, test = data[:split], data[split:]
    Xt, yt = zip(*train)
    Xv, yv = zip(*test)
    return list(Xt), list(Xv), list(yt), list(yv)

# ═══════════════════════════════════════════
# K-Nearest Neighbors
# ═══════════════════════════════════════════
class KNNClassifier:
    """K-Nearest Neighbors classifier. Lazy learning — no explicit training."""

    def __init__(self, k: int = 5, distance=euclidean):
        self.k = k
        self.distance = distance
        self._X: list = []
        self._y: list = []

    def fit(self, X, y) -> "KNNClassifier":
        self._X = list(X)
        self._y = list(y)
        return self

    def predict_one(self, x):
        dists = [(self.distance(x, xi), yi) for xi, yi in zip(self._X, self._y)]
        dists.sort(key=lambda d: d[0])
        k_labels = [label for _, label in dists[:self.k]]
        return Counter(k_labels).most_common(1)[0][0]

    def predict(self, X) -> list:
        return [self.predict_one(x) for x in X]

class KNNRegressor:
    def __init__(self, k: int = 5, distance=euclidean):
        self.k = k
        self.distance = distance
        self._X: list = []
        self._y: list = []

    def fit(self, X, y) -> "KNNRegressor":
        self._X = list(X)
        self._y = list(y)
        return self

    def predict_one(self, x):
        dists = sorted(zip([self.distance(x, xi) for xi in self._X], self._y))
        k_vals = [v for _, v in dists[:self.k]]
        return sum(k_vals) / len(k_vals)

    def predict(self, X) -> list:
        return [self.predict_one(x) for x in X]

# ═══════════════════════════════════════════
# Decision Tree (ID3 / CART simplified)
# ═══════════════════════════════════════════
def gini(labels: list) -> float:
    """Gini impurity."""
    if not labels:
        return 0.0
    n = len(labels)
    counts = Counter(labels)
    return 1.0 - sum((c/n)**2 for c in counts.values())

def entropy(labels: list) -> float:
    if not labels:
        return 0.0
    n = len(labels)
    counts = Counter(labels)
    return -sum((c/n) * math.log2(c/n) for c in counts.values() if c > 0)

def best_split(X: list[list], y: list, criterion="gini"):
    """Find best (feature, threshold) split."""
    measure = gini if criterion == "gini" else entropy
    best_score = float("inf")
    best_feat, best_thresh = None, None

    n, p = len(X), len(X[0])
    for feat in range(p):
        values = sorted(set(row[feat] for row in X))
        thresholds = [(values[i] + values[i+1]) / 2 for i in range(len(values)-1)]
        for thresh in thresholds:
            left_y  = [y[i] for i in range(n) if X[i][feat] <= thresh]
            right_y = [y[i] for i in range(n) if X[i][feat] >  thresh]
            if not left_y or not right_y:
                continue
            score = (len(left_y) * measure(left_y) +
                     len(right_y) * measure(right_y)) / n
            if score < best_score:
                best_score = score
                best_feat, best_thresh = feat, thresh

    return best_feat, best_thresh, best_score

class DTNode:
    def __init__(self, feat=None, thresh=None, left=None, right=None, value=None):
        self.feat = feat; self.thresh = thresh
        self.left = left; self.right = right
        self.value = value  # leaf prediction

class DecisionTreeClassifier:
    def __init__(self, max_depth: int = 5, min_samples: int = 2, criterion="gini"):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.criterion = criterion
        self.root: DTNode | None = None

    def fit(self, X, y) -> "DecisionTreeClassifier":
        self.root = self._build(list(X), list(y), depth=0)
        return self

    def _build(self, X, y, depth) -> DTNode:
        # Stopping criteria
        if depth >= self.max_depth or len(y) < self.min_samples or len(set(y)) == 1:
            return DTNode(value=Counter(y).most_common(1)[0][0])

        feat, thresh, score = best_split(X, y, self.criterion)
        if feat is None:
            return DTNode(value=Counter(y).most_common(1)[0][0])

        left_idx  = [i for i in range(len(X)) if X[i][feat] <= thresh]
        right_idx = [i for i in range(len(X)) if X[i][feat] >  thresh]

        return DTNode(
            feat=feat, thresh=thresh,
            left  = self._build([X[i] for i in left_idx],  [y[i] for i in left_idx],  depth+1),
            right = self._build([X[i] for i in right_idx], [y[i] for i in right_idx], depth+1),
        )

    def _predict_one(self, x, node: DTNode):
        if node.value is not None:
            return node.value
        return (self._predict_one(x, node.left) if x[node.feat] <= node.thresh
                else self._predict_one(x, node.right))

    def predict(self, X) -> list:
        return [self._predict_one(x, self.root) for x in X]

# ═══════════════════════════════════════════
# DEMO: Iris-like dataset (3 classes)
# ═══════════════════════════════════════════
def make_blobs(n_per_class=40, seed=42):
    """Generate 3 Gaussian clusters."""
    random.seed(seed)
    centers = [(2, 2), (7, 3), (5, 8)]
    labels  = [0, 1, 2]
    X, y = [], []
    for center, label in zip(centers, labels):
        for _ in range(n_per_class):
            X.append([center[0] + random.gauss(0, 1),
                      center[1] + random.gauss(0, 1)])
            y.append(label)
    return X, y

if __name__ == "__main__":
    X, y = make_blobs(40)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25)

    print("=== KNN Classifier ===")
    for k in [1, 3, 5, 7]:
        knn = KNNClassifier(k=k).fit(X_tr, y_tr)
        preds = knn.predict(X_te)
        print(f"  k={k}: accuracy={accuracy(y_te, preds):.3f}")

    print("\n=== Decision Tree ===")
    for max_d in [2, 3, 5, 10]:
        dt = DecisionTreeClassifier(max_depth=max_d).fit(X_tr, y_tr)
        preds = dt.predict(X_te)
        print(f"  depth={max_d}: accuracy={accuracy(y_te, preds):.3f}")

    print("\n=== KNN Regressor ===")
    # y = sin(x) + noise
    random.seed(0)
    Xr = [[i/10] for i in range(100)]
    yr = [math.sin(x[0]) + random.gauss(0, 0.1) for x in Xr]
    Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(Xr, yr, test_size=0.2)

    for k in [1, 3, 7]:
        reg = KNNRegressor(k=k).fit(Xr_tr, yr_tr)
        preds = reg.predict(Xr_te)
        mse = sum((p-t)**2 for p,t in zip(preds, yr_te)) / len(yr_te)
        print(f"  k={k}: MSE={mse:.4f}")

    print("\n=== Gini / Entropy ===")
    print(f"  gini([0,0,0,1]): {gini([0,0,0,1]):.4f}")
    print(f"  gini([0,1,0,1]): {gini([0,1,0,1]):.4f} (max=0.5)")
    print(f"  entropy([0,0,0,1]): {entropy([0,0,0,1]):.4f}")
    print(f"  entropy([0,1,0,1]): {entropy([0,1,0,1]):.4f} (max=1.0)")
