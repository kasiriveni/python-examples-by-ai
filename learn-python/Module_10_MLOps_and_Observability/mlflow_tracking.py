"""
This script demonstrates experiment tracking with MLflow.
Topics covered:
1. Logging parameters, metrics, and artifacts.
2. Tracking multiple runs.
"""

import mlflow

# Set the tracking URI (local or remote server)
mlflow.set_tracking_uri("http://localhost:5000")

# Start an MLflow run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("batch_size", 32)

    # Log metrics
    for epoch in range(1, 6):
        accuracy = 0.8 + epoch * 0.02
        mlflow.log_metric("accuracy", accuracy, step=epoch)

    # Log artifacts (e.g., model files, plots)
    with open("output.txt", "w") as f:
        f.write("Experiment output")
    mlflow.log_artifact("output.txt")

print("Experiment logged successfully.")