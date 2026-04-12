"""
This script demonstrates experiment tracking with Weights & Biases (W&B).
Topics covered:
1. Logging parameters, metrics, and artifacts.
2. Tracking multiple runs.
"""

import wandb

# Initialize a W&B run
wandb.init(project="experiment-tracking", name="run-1")

# Log parameters
wandb.config.learning_rate = 0.01
wandb.config.batch_size = 32

# Log metrics
for epoch in range(1, 6):
    accuracy = 0.8 + epoch * 0.02
    wandb.log({"epoch": epoch, "accuracy": accuracy})

# Log artifacts (e.g., model files, plots)
with open("output.txt", "w") as f:
    f.write("Experiment output")
wandb.save("output.txt")

print("Experiment logged successfully.")
