"""
Machine Learning and AI: Linear Regression from scratch + scikit-learn patterns.
Implements gradient descent, normal equation, and feature engineering.
"""
import math
import random
from typing import Callable

# ═══════════════════════════════════════════
# Utility — pure numeric (no numpy)
# ═══════════════════════════════════════════
def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def mat_vec(M: list[list[float]], v: list[float]) -> list[float]:
    return [dot(row, v) for row in M]

def transpose(M: list[list[float]]) -> list[list[float]]:
    return [[M[r][c] for r in range(len(M))] for c in range(len(M[0]))]

def mat_mul(A, B):
    Bt = transpose(B)
    return [[dot(row_a, col_b) for col_b in Bt] for row_a in A]

def mat_inv_2x2(M):
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    det = a*d - b*c
    if abs(det) < 1e-10:
        raise ValueError("Matrix is singular")
    return [[d/det, -b/det], [-c/det, a/det]]

# ═══════════════════════════════════════════
# Simple Linear Regression (OLS)
# ═══════════════════════════════════════════
class SimpleLinearRegression:
    """y = w1*x + w0 via closed-form solution."""

    def __init__(self):
        self.w0 = 0.0  # intercept
        self.w1 = 0.0  # slope

    def fit(self, X: list[float], y: list[float]) -> "SimpleLinearRegression":
        n = len(X)
        x_mean = sum(X) / n
        y_mean = sum(y) / n

        numer = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(X, y))
        denom = sum((xi - x_mean)**2 for xi in X)
        self.w1 = numer / denom
        self.w0 = y_mean - self.w1 * x_mean
        return self

    def predict(self, X: list[float]) -> list[float]:
        return [self.w1 * x + self.w0 for x in X]

    def score(self, X: list[float], y: list[float]) -> float:
        """R² score."""
        y_pred = self.predict(X)
        y_mean = sum(y) / len(y)
        ss_res = sum((yi - yp)**2 for yi, yp in zip(y, y_pred))
        ss_tot = sum((yi - y_mean)**2 for yi in y)
        return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    def __repr__(self):
        return f"LinearRegression(slope={self.w1:.4f}, intercept={self.w0:.4f})"

# ═══════════════════════════════════════════
# Gradient Descent Linear Regression
# ═══════════════════════════════════════════
class GradientDescentRegressor:
    """Linear regression via batch gradient descent."""

    def __init__(self, lr: float = 0.01, n_iter: int = 1000):
        self.lr = lr
        self.n_iter = n_iter
        self.weights: list[float] = []
        self.losses: list[float] = []

    def fit(self, X: list[list[float]], y: list[float]) -> "GradientDescentRegressor":
        n, p = len(X), len(X[0]) + 1  # +1 for bias
        X_b = [[1.0] + row for row in X]  # add bias column
        self.weights = [0.0] * p

        for _ in range(self.n_iter):
            y_hat = [dot(row, self.weights) for row in X_b]
            errors = [yh - yi for yh, yi in zip(y_hat, y)]
            loss = sum(e**2 for e in errors) / (2 * n)
            self.losses.append(loss)
            # Gradient update
            for j in range(p):
                grad = sum(e * row[j] for e, row in zip(errors, X_b)) / n
                self.weights[j] -= self.lr * grad

        return self

    def predict(self, X: list[list[float]]) -> list[float]:
        X_b = [[1.0] + row for row in X]
        return [dot(row, self.weights) for row in X_b]

# ═══════════════════════════════════════════
# Polynomial Feature Engineering
# ═══════════════════════════════════════════
def poly_features(X: list[float], degree: int) -> list[list[float]]:
    """Transform 1D X to polynomial features [x, x², x³, ...]."""
    return [[x**d for d in range(1, degree + 1)] for x in X]

# ═══════════════════════════════════════════
# Metrics
# ═══════════════════════════════════════════
def mse(y_true, y_pred):
    return sum((t - p)**2 for t, p in zip(y_true, y_pred)) / len(y_true)

def rmse(y_true, y_pred):
    return math.sqrt(mse(y_true, y_pred))

def mae(y_true, y_pred):
    return sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true)

def r2_score(y_true, y_pred):
    mean_y = sum(y_true) / len(y_true)
    ss_res = sum((t - p)**2 for t, p in zip(y_true, y_pred))
    ss_tot = sum((t - mean_y)**2 for t in y_true)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
def generate_data(n=100, noise=5.0, seed=42):
    """y = 3x + 7 + noise"""
    random.seed(seed)
    X = [random.uniform(0, 50) for _ in range(n)]
    y = [3 * x + 7 + random.gauss(0, noise) for x in X]
    return X, y

if __name__ == "__main__":
    print("=== Simple Linear Regression (OLS) ===")
    X, y = generate_data()

    slr = SimpleLinearRegression().fit(X, y)
    y_pred = slr.predict(X)
    print(slr)
    print(f"R²:   {slr.score(X, y):.4f}")
    print(f"MSE:  {mse(y, y_pred):.2f}")
    print(f"RMSE: {rmse(y, y_pred):.2f}")
    print(f"MAE:  {mae(y, y_pred):.2f}")

    print("\n=== Gradient Descent Regression ===")
    # Normalise
    x_mean = sum(X) / len(X)
    x_std = math.sqrt(sum((x - x_mean)**2 for x in X) / len(X))
    X_norm = [[(x - x_mean) / x_std] for x in X]

    gdr = GradientDescentRegressor(lr=0.1, n_iter=200)
    gdr.fit(X_norm, y)
    gd_pred = gdr.predict(X_norm)
    print(f"Weights: {[f'{w:.4f}' for w in gdr.weights]}")
    print(f"R²:      {r2_score(y, gd_pred):.4f}")
    print(f"Initial loss: {gdr.losses[0]:.2f}  →  Final: {gdr.losses[-1]:.2f}")

    print("\n=== Polynomial Regression (degree=2) ===")
    # Generate non-linear data: y = x² + noise
    random.seed(0)
    X_nl = [random.uniform(-3, 3) for _ in range(80)]
    y_nl = [x**2 + random.gauss(0, 0.5) for x in X_nl]

    X_poly = poly_features(X_nl, degree=2)
    gdr2 = GradientDescentRegressor(lr=0.1, n_iter=500)
    gdr2.fit(X_poly, y_nl)
    poly_pred = gdr2.predict(X_poly)
    print(f"Poly R²: {r2_score(y_nl, poly_pred):.4f}")

    print("\n=== Sample Predictions ===")
    test_X = [0, 10, 25, 40, 50]
    test_pred = slr.predict(test_X)
    for xi, yp in zip(test_X, test_pred):
        print(f"  x={xi:4d}  →  y_pred={yp:.2f}  (true≈{3*xi+7})")
