"""
Machine Learning and AI: Naive Bayes and neural network from scratch.
"""
import math
import random
from collections import defaultdict
from typing import Sequence

# ═══════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════
def train_test_split(X, y, test_size=0.2, seed=42):
    data = list(zip(X, y))
    random.seed(seed)
    random.shuffle(data)
    n = int(len(data) * (1 - test_size))
    train, test = data[:n], data[n:]
    Xt, yt = zip(*train); Xv, yv = zip(*test)
    return list(Xt), list(Xv), list(yt), list(yv)

def accuracy(y_true, y_pred) -> float:
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)

# ═══════════════════════════════════════════
# 1. Gaussian Naive Bayes
# ═══════════════════════════════════════════
class GaussianNaiveBayes:
    """P(y|x) ∝ P(y) * ∏ P(xi|y),  P(xi|y) ~ Gaussian"""

    def fit(self, X, y) -> "GaussianNaiveBayes":
        from collections import Counter
        n = len(y)
        classes = sorted(set(y))
        self._classes = classes

        # Class priors
        counts = Counter(y)
        self._log_prior = {c: math.log(counts[c] / n) for c in classes}

        # Per-class, per-feature: mean and variance
        self._stats: dict[any, list[tuple[float, float]]] = {}
        for c in classes:
            Xi = [X[i] for i in range(n) if y[i] == c]
            p = len(Xi[0])
            stats = []
            for j in range(p):
                col = [Xi[i][j] for i in range(len(Xi))]
                m = sum(col) / len(col)
                s2 = sum((x - m)**2 for x in col) / max(len(col) - 1, 1)
                stats.append((m, s2 + 1e-9))  # add epsilon to avoid zero variance
            self._stats[c] = stats
        return self

    def _log_likelihood(self, x: list, c) -> float:
        ll = 0.0
        for j, xj in enumerate(x):
            mu, var = self._stats[c][j]
            ll += -0.5 * math.log(2 * math.pi * var) - (xj - mu)**2 / (2 * var)
        return ll

    def predict_one(self, x) -> any:
        scores = {c: self._log_prior[c] + self._log_likelihood(x, c)
                  for c in self._classes}
        return max(scores, key=scores.__getitem__)

    def predict(self, X) -> list:
        return [self.predict_one(x) for x in X]

    def predict_proba(self, x) -> dict:
        """Return class probabilities (normalised log-softmax)."""
        log_scores = {c: self._log_prior[c] + self._log_likelihood(x, c)
                      for c in self._classes}
        max_log = max(log_scores.values())
        raw = {c: math.exp(v - max_log) for c, v in log_scores.items()}
        total = sum(raw.values())
        return {c: v / total for c, v in raw.items()}

# ═══════════════════════════════════════════
# 2. Multinomial Naive Bayes (for text)
# ═══════════════════════════════════════════
class MultinomialNaiveBayes:
    """Naive Bayes for count or frequency features (e.g. bag-of-words)."""

    def __init__(self, alpha: float = 1.0):  # Laplace smoothing
        self.alpha = alpha

    def fit(self, X, y) -> "MultinomialNaiveBayes":
        from collections import Counter
        n = len(y)
        classes = sorted(set(y))
        self._classes = classes
        p = len(X[0])

        counts = Counter(y)
        self._log_prior = {c: math.log(counts[c] / n) for c in classes}

        self._log_cond: dict[any, list[float]] = {}
        for c in classes:
            Xi = [X[i] for i in range(n) if y[i] == c]
            feature_totals = [sum(xi[j] for xi in Xi) + self.alpha for j in range(p)]
            total = sum(feature_totals)
            self._log_cond[c] = [math.log(ft / total) for ft in feature_totals]
        return self

    def predict_one(self, x) -> any:
        scores = {}
        for c in self._classes:
            scores[c] = self._log_prior[c] + sum(
                x[j] * self._log_cond[c][j] for j in range(len(x)) if x[j] > 0
            )
        return max(scores, key=scores.__getitem__)

    def predict(self, X) -> list:
        return [self.predict_one(x) for x in X]

# ═══════════════════════════════════════════
# 3. Simple feedforward neural network
# ═══════════════════════════════════════════
def sigmoid(x): return 1 / (1 + math.exp(-max(-500, min(500, x))))
def relu(x):    return max(0, x)
def relu_d(x):  return 1 if x > 0 else 0

def dot(a, b):  return sum(x*y for x, y in zip(a, b))
def mat_vec(M, v): return [dot(row, v) for row in M]

class NeuralNetwork:
    """
    Shallow NN: input → hidden (relu) → output (sigmoid).
    Binary classification.
    """

    def __init__(self, n_inputs: int, n_hidden: int, lr: float = 0.1, seed: int = 0):
        random.seed(seed)
        scale = math.sqrt(2 / n_inputs)  # He initialisation for ReLU

        self.W1 = [[random.gauss(0, scale) for _ in range(n_inputs)]  for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [random.gauss(0, scale/math.sqrt(n_hidden)) for _ in range(n_hidden)]
        self.b2 = 0.0
        self.lr = lr

    def _forward(self, x):
        # Hidden layer
        z1 = [dot(self.W1[j], x) + self.b1[j] for j in range(len(self.b1))]
        a1 = [relu(z) for z in z1]
        # Output
        z2 = dot(self.W2, a1) + self.b2
        a2 = sigmoid(z2)
        return z1, a1, z2, a2

    def predict_prob(self, x) -> float:
        _, _, _, a2 = self._forward(x)
        return a2

    def predict(self, X) -> list[int]:
        return [1 if self.predict_prob(x) >= 0.5 else 0 for x in X]

    def train_step(self, x, y_true: float) -> float:
        z1, a1, z2, a2 = self._forward(x)

        # Binary cross-entropy loss
        eps = 1e-12
        loss = -(y_true * math.log(a2 + eps) + (1-y_true) * math.log(1-a2 + eps))

        # Backprop: output layer
        dL_dz2 = a2 - y_true          # sigmoid + BCE gradient

        # Update W2, b2
        for j in range(len(self.W2)):
            self.W2[j] -= self.lr * dL_dz2 * a1[j]
        self.b2 -= self.lr * dL_dz2

        # Backprop: hidden layer
        for j in range(len(self.b1)):
            dL_dz1 = dL_dz2 * self.W2[j] * relu_d(z1[j])
            for k in range(len(x)):
                self.W1[j][k] -= self.lr * dL_dz1 * x[k]
            self.b1[j] -= self.lr * dL_dz1

        return loss

    def fit(self, X, y, epochs=100) -> list[float]:
        losses = []
        for epoch in range(epochs):
            epoch_loss = 0.0
            data = list(zip(X, y))
            random.shuffle(data)
            for xi, yi in data:
                epoch_loss += self.train_step(xi, float(yi))
            losses.append(epoch_loss / len(data))
        return losses

if __name__ == "__main__":
    from contextlib import suppress

    # Blobs dataset
    def make_blobs(n=100, seed=0):
        random.seed(seed)
        X, y = [], []
        for _ in range(n):
            if random.random() > 0.5:
                X.append([random.gauss(2, 1), random.gauss(2, 1)]); y.append(0)
            else:
                X.append([random.gauss(7, 1), random.gauss(7, 1)]); y.append(1)
        return X, y

    X, y = make_blobs(200)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y)

    print("=== Gaussian Naive Bayes ===")
    gnb = GaussianNaiveBayes().fit(X_tr, y_tr)
    preds = gnb.predict(X_te)
    print(f"  Accuracy: {accuracy(y_te, preds):.3f}")
    proba = gnb.predict_proba(X_te[0])
    print(f"  P(class|x[0]): {proba}")

    print("\n=== Multinomial NB (bag-of-words) ===")
    # Vocabulary: ["buy", "cheap", "hello", "friend", "free", "discount"]
    # Spam=1, Ham=0
    vocab_data = [
        ([2,3,0,0,1,2], 1),  # spam
        ([0,0,1,1,0,0], 0),  # ham
        ([1,0,0,1,0,0], 0),
        ([3,2,0,0,2,1], 1),
        ([0,0,2,1,0,0], 0),
        ([2,1,0,0,1,3], 1),
    ]
    Xm, ym = zip(*vocab_data)
    mnb = MultinomialNaiveBayes(alpha=1.0).fit(list(Xm), list(ym))
    test_msg = [2, 2, 0, 0, 1, 2]  # looks spammy
    pred = mnb.predict_one(test_msg)
    print(f"  '{test_msg}' → {'spam' if pred else 'ham'}")

    print("\n=== Neural Network ===")
    nn = NeuralNetwork(n_inputs=2, n_hidden=8, lr=0.05)
    losses = nn.fit(X_tr, y_tr, epochs=50)
    preds = nn.predict(X_te)
    print(f"  Accuracy: {accuracy(y_te, preds):.3f}")
    print(f"  Loss epoch 1:  {losses[0]:.4f}")
    print(f"  Loss epoch 50: {losses[-1]:.4f}")

    # XOR problem
    Xxor = [[0,0],[0,1],[1,0],[1,1]]
    yxor = [0, 1, 1, 0]
    nn2 = NeuralNetwork(n_inputs=2, n_hidden=4, lr=0.5)
    losses2 = nn2.fit(Xxor * 500, yxor * 500, epochs=200)
    preds2 = nn2.predict(Xxor)
    print(f"\n  XOR preds: {preds2} (expected {yxor})")
    print(f"  XOR accuracy: {accuracy(yxor, preds2):.3f}")
