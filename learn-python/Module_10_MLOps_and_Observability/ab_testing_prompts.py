"""
This script demonstrates A/B testing for LLM prompts.
Topics covered:
1. Comparing the effectiveness of two prompts.
2. Logging and analyzing results.
"""

import random

# Define two prompts for A/B testing
prompt_a = "What is the capital of France?"
prompt_b = "Name the capital city of France."

# Simulate LLM responses
def simulate_llm_response(prompt):
    if "capital" in prompt:
        return "The capital of France is Paris."
    return "Unknown response."

# Conduct A/B testing
results = {"A": 0, "B": 0}
for _ in range(100):
    chosen_prompt = random.choice(["A", "B"])
    prompt = prompt_a if chosen_prompt == "A" else prompt_b
    response = simulate_llm_response(prompt)
    if "Paris" in response:
        results[chosen_prompt] += 1

print("A/B Testing Results:", results)
