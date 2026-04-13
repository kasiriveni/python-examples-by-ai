"""
Machine Learning and AI: Data Preprocessing.
Feature scaling, encoding, train-test split, cross-validation — pure Python.
"""
import math
import random
from collections import Counter

# ═══════════════════════════════════════════
# Train / Test Split
# ═══════════════════════════════════════════
def train_test_split(X, y, test_size=0.2, shuffle=True, seed=42):
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")
    data = list(zip(X, y))
    if shuffle:
        random.seed(seed)
        random.shuffle(data)
    split = int(len(data) * (1 - test_size))
    train, test = data[:split], data[split:]
    X_train, y_train = zip(*train) if train else ([], [])
    X_test, y_test   = zip(*test)  if test  else ([], [])
    return list(X_train), list(X_test), list(y_train), list(y_test)

# ═══════════════════════════════════════════
# Feature Scaling
# ═══════════════════════════════════════════
class StandardScaler:
    """Standardize: z = (x - mean) / std"""
    def __init__(self):
        self.mean_: list[float] = []
        self.std_: list[float] = []

    def fit(self, X: list[list[float]]) -> "StandardScaler":
        n = len(X)
        p = len(X[0])
        self.mean_ = [sum(row[j] for row in X) / n for j in range(p)]
        self.std_  = [
            math.sqrt(sum((row[j] - self.mean_[j])**2 for row in X) / n)
            for j in range(p)
        ]
        # Replace 0 stds to avoid division by zero
        self.std_ = [s if s > 0 else 1.0 for s in self.std_]
        return self

    def transform(self, X: list[list[float]]) -> list[list[float]]:
        return [[(x - m) / s for x, m, s in zip(row, self.mean_, self.std_)] for row in X]

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, X: list[list[float]]) -> list[list[float]]:
        return [[x * s + m for x, m, s in zip(row, self.mean_, self.std_)] for row in X]

class MinMaxScaler:
    """Scale features to [0, 1]: x_scaled = (x - min) / (max - min)"""
    def __init__(self):
        self.min_: list[float] = []
        self.max_: list[float] = []

    def fit(self, X: list[list[float]]) -> "MinMaxScaler":
        p = len(X[0])
        self.min_ = [min(row[j] for row in X) for j in range(p)]
        self.max_ = [max(row[j] for row in X) for j in range(p)]
        return self

    def transform(self, X: list[list[float]]) -> list[list[float]]:
        result = []
        for row in X:
            scaled = []
            for x, lo, hi in zip(row, self.min_, self.max_):
                denom = hi - lo
                scaled.append((x - lo) / denom if denom > 0 else 0.0)
            result.append(scaled)
        return result

    def fit_transform(self, X):
        return self.fit(X).transform(X)

# ═══════════════════════════════════════════
# Categorical Encoding
# ═══════════════════════════════════════════
class LabelEncoder:
    """Encode categorical labels as integers."""
    def __init__(self):
        self.classes_: list = []
        self._map: dict = {}

    def fit(self, y: list) -> "LabelEncoder":
        self.classes_ = sorted(set(y))
        self._map = {c: i for i, c in enumerate(self.classes_)}
        return self

    def transform(self, y: list) -> list[int]:
        return [self._map[v] for v in y]

    def fit_transform(self, y):
        return self.fit(y).transform(y)

    def inverse_transform(self, y: list[int]) -> list:
        return [self.classes_[i] for i in y]

class OneHotEncoder:
    """One-hot encode a categorical column."""
    def __init__(self):
        self.categories_: list = []
        self._map: dict = {}

    def fit(self, y: list) -> "OneHotEncoder":
        self.categories_ = sorted(set(y))
        self._map = {c: i for i, c in enumerate(self.categories_)}
        return self

    def transform(self, y: list) -> list[list[int]]:
        n = len(self.categories_)
        return [[1 if i == self._map[v] else 0 for i in range(n)] for v in y]

    def fit_transform(self, y):
        return self.fit(y).transform(y)

# ═══════════════════════════════════════════
# Missing Value Imputation
# ═══════════════════════════════════════════
class SimpleImputer:
    """Fill missing values (None or NaN)."""

    def __init__(self, strategy: str = "mean"):
        assert strategy in ("mean", "median", "mode", "constant")
        self.strategy = strategy
        self.fill_values_: list = []

    def fit(self, X: list[list]) -> "SimpleImputer":
        p = len(X[0])
        self.fill_values_ = []
        for j in range(p):
            col = [row[j] for row in X if row[j] is not None and row[j] == row[j]]
            if not col:
                self.fill_values_.append(0)
                continue
            if self.strategy == "mean":
                self.fill_values_.append(sum(col) / len(col))
            elif self.strategy == "median":
                s = sorted(col)
                mid = len(s) // 2
                self.fill_values_.append(s[mid] if len(s) % 2 else (s[mid-1] + s[mid]) / 2)
            elif self.strategy == "mode":
                self.fill_values_.append(Counter(col).most_common(1)[0][0])
            else:
                self.fill_values_.append(0)
        return self

    def transform(self, X: list[list]) -> list[list]:
        return [
            [v if v is not None and v == v else self.fill_values_[j]
             for j, v in enumerate(row)]
            for row in X
        ]

    def fit_transform(self, X):
        return self.fit(X).transform(X)

# ═══════════════════════════════════════════
# K-Fold Cross Validation
# ═══════════════════════════════════════════
def k_fold_split(X, y, k=5, shuffle=True, seed=42):
    """Yield (X_train, X_val, y_train, y_val) for each fold."""
    data = list(zip(X, y))
    if shuffle:
        random.seed(seed)
        random.shuffle(data)
    fold_size = len(data) // k
    for fold in range(k):
        val   = data[fold*fold_size : (fold+1)*fold_size]
        train = data[:fold*fold_size] + data[(fold+1)*fold_size:]
        Xt, yt = zip(*train)
        Xv, yv = zip(*val)
        yield list(Xt), list(Xv), list(yt), list(yv)

if __name__ == "__main__":
    random.seed(0)
    print("=== Train/Test Split ===")
    X = [[random.gauss(0, 1), random.gauss(0, 1)] for _ in range(100)]
    y = [1 if sum(row) > 0 else 0 for row in X]

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)
    print(f"Train: {len(X_tr)}, Test: {len(X_te)}")
    print(f"Train label dist: {Counter(y_tr)}")

    print("\n=== StandardScaler ===")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_tr)
    feat_means = [sum(row[j] for row in X_scaled)/len(X_scaled) for j in range(2)]
    feat_stds  = [math.sqrt(sum((row[j]-feat_means[j])**2 for row in X_scaled)/len(X_scaled)) for j in range(2)]
    print(f"Means after scaling: {[f'{m:.6f}' for m in feat_means]}")
    print(f"Stds after scaling:  {[f'{s:.4f}' for s in feat_stds]}")

    print("\n=== MinMaxScaler ===")
    mm = MinMaxScaler()
    X_mm = mm.fit_transform([[1, 10], [2, 20], [3, 30], [4, 40]])
    print(f"MinMax scaled: {X_mm}")

    print("\n=== LabelEncoder ===")
    labels = ["cat", "dog", "cat", "bird", "dog", "bird"]
    le = LabelEncoder()
    encoded = le.fit_transform(labels)
    print(f"Classes: {le.classes_}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {le.inverse_transform(encoded)}")

    print("\n=== OneHotEncoder ===")
    ohe = OneHotEncoder()
    oh = ohe.fit_transform(["red", "green", "blue", "red"])
    print(f"Categories: {ohe.categories_}")
    for label, vec in zip(["red", "green", "blue", "red"], oh):
        print(f"  {label} -> {vec}")

    print("\n=== SimpleImputer ===")
    X_missing = [[1.0, None], [2.0, 3.0], [None, 4.0], [4.0, 5.0]]
    imp = SimpleImputer(strategy="mean")
    X_filled = imp.fit_transform(X_missing)
    print(f"Fill values: {imp.fill_values_}")
    print(f"Filled: {X_filled}")

    print("\n=== K-Fold CV ===")
    for fold_idx, (Xt, Xv, yt, yv) in enumerate(k_fold_split(X, y, k=5)):
        print(f"  Fold {fold_idx}: train={len(Xt)}, val={len(Xv)}, val_pos={sum(yv)}")
