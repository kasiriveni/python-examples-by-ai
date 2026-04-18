# Core Python Concepts

## Core Themes
- Experiment tracking and model observability.
- Prompt versioning, serving, fine-tuning, and cost management.
- Evaluation and comparison of production ML and LLM systems.

## Core Theme Examples
- Example 1: MLflow experiment runs with metrics and artifact logging.
- Example 2: Prompt versioning and A/B testing comparisons.
- Example 3: Token-based cost tracking and API optimization.

## Files and Concepts
- ab_testing_prompts.py: A B testing, prompt comparison, experiment analysis
- cost_monitoring_optimization.py: token tracking, cost calculation, optimization strategies
- fine_tuning_lora_peft.py: LoRA, PEFT, parameter-efficient fine-tuning
- huggingface_libraries.py: transformers, datasets, inference pipelines
- llm_observability.py: LangSmith, Langfuse, Helicone-style logging and tracing
- mlflow_tracking.py: MLflow runs, metrics, artifacts, experiment logging
- mlops_patterns.py: prediction logs, monitoring metrics, model-monitor patterns
- model_serving_vllm.py: vLLM serving, inference requests, hosted model execution
- prompt_versioning.py: prompt managers, version metadata, prompt lifecycle control
- wandb_tracking.py: Weights and Biases experiment tracking

## Core Example
This example records model metrics in a small experiment log.

```python
run = {
	"name": "demo-run",
	"metrics": {"accuracy": 0.91, "loss": 0.12},
}

for key, value in run["metrics"].items():
	print(f"{key}={value}")
```
