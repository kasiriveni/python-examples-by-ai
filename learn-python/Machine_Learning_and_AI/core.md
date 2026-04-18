# Core Python Concepts

## Core Themes
- Introductory machine-learning algorithms and preprocessing.
- Model training, evaluation, and feature handling.
- From-scratch and library-assisted learning examples.

## Core Theme Examples
- Example 1: K-Nearest Neighbors classification with distance metrics.
- Example 2: Train-test splitting and accuracy evaluation.
- Example 3: Random Forest classification with scikit-learn.

## Files and Concepts
- classification_basics.py: KNN, decision trees, train-test split, accuracy
- clustering.py: K-Means, centroid updates, K-Means-plus-plus style initialization
- data_preprocessing.py: StandardScaler, feature scaling, train-test split, cross-validation
- knn_and_decision_tree.py: distance-based classification, tree-based prediction, accuracy metrics
- linear_regression.py: ordinary least squares, gradient descent, normal equations, feature engineering
- naive_bayes_neural_net.py: Gaussian Naive Bayes, neural networks, activation functions, probabilities
- simple_ml_example.py: RandomForest, iris dataset, model evaluation

## Core Example
This example uses a tiny nearest-neighbor style classifier in pure Python.

```python
from math import dist

samples = [([1, 1], "A"), ([5, 5], "B")]
query = [2, 2]

label = min(samples, key=lambda item: dist(item[0], query))[1]
print(label)
```
