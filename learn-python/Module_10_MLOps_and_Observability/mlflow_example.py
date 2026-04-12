# Example: MLflow for Experiment Tracking
# Demonstrates how to log metrics and parameters with MLflow

import mlflow

# Start an MLflow run
with mlflow.start_run():
    mlflow.log_param("param1", 5)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)

    print("Metrics logged to MLflow.")