"""
This script demonstrates using HuggingFace transformers and datasets libraries.
Topics covered:
1. Loading a pre-trained model and tokenizer.
2. Using the datasets library to load and preprocess data.
"""

from transformers import pipeline
from datasets import load_dataset

# Load a pre-trained model pipeline
classifier = pipeline("sentiment-analysis")

# Use the pipeline
result = classifier("I love using HuggingFace libraries!")
print("Sentiment Analysis Result:", result)

# Load a dataset
dataset = load_dataset("imdb", split="train[:100]")

# Preprocess the dataset
def preprocess_function(examples):
    return {"text": examples["text"].lower()}

processed_dataset = dataset.map(preprocess_function)
print("Processed Dataset Example:", processed_dataset[0])
