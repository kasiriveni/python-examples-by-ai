"""
Machine Learning and AI: Classification fundamentals.
"""
import math
import random
from collections import Counter

# === K-Nearest Neighbors (from scratch) ===
class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = []
        self.y_train = []

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def _distance(self, a, b):
        return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

    def predict_one(self, x):
        distances = [(self._distance(x, xi), yi) for xi, yi in zip(self.X_train, self.y_train)]
        distances.sort(key=lambda d: d[0])
        k_nearest = [label for _, label in distances[:self.k]]
        return Counter(k_nearest).most_common(1)[0][0]

    def predict(self, X):
        return [self.predict_one(x) for x in X]

    def score(self, X, y):
        predictions = self.predict(X)
        correct = sum(1 for p, a in zip(predictions, y) if p == a)
        return correct / len(y)

# === Decision Tree (simplified) ===
class DecisionNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # Leaf prediction

class SimpleDecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.root = None

    def _gini(self, y):
        counts = Counter(y)
        n = len(y)
        return 1 - sum((c / n) ** 2 for c in counts.values())

    def _best_split(self, X, y):
        best_gini = float('inf')
        best_feature, best_threshold = None, None

        n_features = len(X[0])
        for feature in range(n_features):
            values = sorted(set(row[feature] for row in X))
            for i in range(len(values) - 1):
                threshold = (values[i] + values[i + 1]) / 2
                left_y = [yi for xi, yi in zip(X, y) if xi[feature] <= threshold]
                right_y = [yi for xi, yi in zip(X, y) if xi[feature] > threshold]

                if not left_y or not right_y:
                    continue

                gini = (len(left_y) * self._gini(left_y) + len(right_y) * self._gini(right_y)) / len(y)
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def _build(self, X, y, depth):
        if depth >= self.max_depth or len(set(y)) == 1 or len(y) < 2:
            return DecisionNode(value=Counter(y).most_common(1)[0][0])

        feature, threshold = self._best_split(X, y)
        if feature is None:
            return DecisionNode(value=Counter(y).most_common(1)[0][0])

        left_mask = [xi[feature] <= threshold for xi in X]
        left_X = [xi for xi, m in zip(X, left_mask) if m]
        left_y = [yi for yi, m in zip(y, left_mask) if m]
        right_X = [xi for xi, m in zip(X, left_mask) if not m]
        right_y = [yi for yi, m in zip(y, left_mask) if not m]

        return DecisionNode(
            feature=feature, threshold=threshold,
            left=self._build(left_X, left_y, depth + 1),
            right=self._build(right_X, right_y, depth + 1),
        )

    def fit(self, X, y):
        self.root = self._build(X, y, 0)

    def _predict_one(self, node, x):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_one(node.left, x)
        return self._predict_one(node.right, x)

    def predict(self, X):
        return [self._predict_one(self.root, x) for x in X]

# === Confusion Matrix ===
def confusion_matrix(y_true, y_pred, labels):
    matrix = {a: {b: 0 for b in labels} for a in labels}
    for true, pred in zip(y_true, y_pred):
        matrix[true][pred] += 1
    return matrix

def print_metrics(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels)
    print("\nConfusion Matrix:")
    print(f"{'':>10}", *[f"{l:>8}" for l in labels])
    for label in labels:
        print(f"{label:>10}", *[f"{cm[label][p]:>8}" for p in labels])

    accuracy = sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)
    print(f"\nAccuracy: {accuracy:.2%}")

if __name__ == "__main__":
    # Generate sample data (2 classes, 2 features)
    random.seed(42)
    X_train, y_train = [], []
    for _ in range(50):
        X_train.append([random.gauss(2, 1), random.gauss(2, 1)])
        y_train.append("A")
    for _ in range(50):
        X_train.append([random.gauss(5, 1), random.gauss(5, 1)])
        y_train.append("B")

    X_test, y_test = [], []
    for _ in range(20):
        X_test.append([random.gauss(2, 1), random.gauss(2, 1)])
        y_test.append("A")
    for _ in range(20):
        X_test.append([random.gauss(5, 1), random.gauss(5, 1)])
        y_test.append("B")

    # KNN
    print("=== K-Nearest Neighbors ===")
    knn = KNN(k=5)
    knn.fit(X_train, y_train)
    knn_preds = knn.predict(X_test)
    print(f"KNN Accuracy: {knn.score(X_test, y_test):.2%}")
    print_metrics(y_test, knn_preds, ["A", "B"])

    # Decision Tree
    print("\n=== Decision Tree ===")
    tree = SimpleDecisionTree(max_depth=3)
    tree.fit(X_train, y_train)
    tree_preds = tree.predict(X_test)
    accuracy = sum(1 for t, p in zip(y_test, tree_preds) if t == p) / len(y_test)
    print(f"Tree Accuracy: {accuracy:.2%}")
    print_metrics(y_test, tree_preds, ["A", "B"])
