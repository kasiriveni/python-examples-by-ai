"""
Module 10: MLOps and Observability - monitoring ML systems.
"""
import time
import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

# === Model Metrics Tracker ===
print("=== Model Metrics ===")

@dataclass
class PredictionLog:
    timestamp: str
    input_data: dict
    prediction: float
    latency_ms: float
    model_version: str

class ModelMonitor:
    def __init__(self, model_name):
        self.model_name = model_name
        self.predictions = []
        self.metrics_history = []

    def log_prediction(self, input_data, prediction, latency_ms, model_version="v1"):
        log = PredictionLog(
            timestamp=datetime.now().isoformat(),
            input_data=input_data,
            prediction=prediction,
            latency_ms=latency_ms,
            model_version=model_version,
        )
        self.predictions.append(log)

    def compute_metrics(self, window=None):
        preds = self.predictions[-window:] if window else self.predictions
        if not preds:
            return {}

        latencies = [p.latency_ms for p in preds]
        predictions = [p.prediction for p in preds]

        metrics = {
            "count": len(preds),
            "avg_latency_ms": statistics.mean(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "prediction_mean": statistics.mean(predictions),
            "prediction_std": statistics.stdev(predictions) if len(predictions) > 1 else 0,
        }
        self.metrics_history.append({"timestamp": datetime.now().isoformat(), **metrics})
        return metrics

    def detect_drift(self, baseline_mean, threshold=0.2):
        if not self.predictions:
            return False
        current_mean = statistics.mean([p.prediction for p in self.predictions[-100:]])
        drift = abs(current_mean - baseline_mean) / baseline_mean
        return drift > threshold, drift

monitor = ModelMonitor("sentiment-classifier")
import random
random.seed(42)
for i in range(50):
    monitor.log_prediction(
        input_data={"text": f"sample_{i}"},
        prediction=random.gauss(0.7, 0.1),
        latency_ms=random.gauss(50, 10),
    )

metrics = monitor.compute_metrics()
print(json.dumps(metrics, indent=2))

has_drift, drift_amount = monitor.detect_drift(0.7)
print(f"\nDrift detected: {has_drift} (amount: {drift_amount:.3f})")

# === A/B Testing Framework ===
print("\n=== A/B Testing ===")

class ABTest:
    def __init__(self, name, variants):
        self.name = name
        self.variants = variants
        self.results = {v: {"conversions": 0, "impressions": 0} for v in variants}

    def assign_variant(self, user_id):
        return self.variants[hash(user_id) % len(self.variants)]

    def record(self, variant, converted=False):
        self.results[variant]["impressions"] += 1
        if converted:
            self.results[variant]["conversions"] += 1

    def analyze(self):
        analysis = {}
        for variant, data in self.results.items():
            rate = data["conversions"] / data["impressions"] if data["impressions"] > 0 else 0
            analysis[variant] = {
                **data,
                "conversion_rate": f"{rate:.2%}",
            }
        return analysis

test = ABTest("model_comparison", ["model_v1", "model_v2"])
for i in range(200):
    variant = test.assign_variant(f"user_{i}")
    converted = random.random() < (0.15 if variant == "model_v1" else 0.20)
    test.record(variant, converted)

print(json.dumps(test.analyze(), indent=2))

# === Pipeline Orchestration ===
print("\n=== ML Pipeline ===")

class PipelineStep:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def run(self, data):
        start = time.perf_counter()
        result = self.func(data)
        elapsed = time.perf_counter() - start
        print(f"  [{self.name}] completed in {elapsed:.4f}s")
        return result

class MLPipeline:
    def __init__(self, name):
        self.name = name
        self.steps = []

    def add_step(self, name, func):
        self.steps.append(PipelineStep(name, func))
        return self

    def run(self, data):
        print(f"Running pipeline: {self.name}")
        result = data
        for step in self.steps:
            result = step.run(result)
        print(f"Pipeline complete!")
        return result

# Define pipeline
pipeline = MLPipeline("training_pipeline")
pipeline.add_step("load_data", lambda d: {**d, "loaded": True})
pipeline.add_step("preprocess", lambda d: {**d, "processed": True})
pipeline.add_step("train", lambda d: {**d, "trained": True, "accuracy": 0.95})
pipeline.add_step("evaluate", lambda d: {**d, "evaluated": True})

result = pipeline.run({"dataset": "training_data"})
print(f"Result: {result}")
