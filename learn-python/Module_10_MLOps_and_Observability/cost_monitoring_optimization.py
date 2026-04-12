"""
This script demonstrates cost monitoring and token optimization for LLM usage.
Topics covered:
1. Tracking token usage.
2. Optimizing prompts to reduce costs.
"""

class TokenTracker:
    def __init__(self):
        self.total_tokens = 0
        self.cost_per_token = 0.0001  # Example cost per token

    def log_tokens(self, tokens):
        self.total_tokens += tokens

    def calculate_cost(self):
        return self.total_tokens * self.cost_per_token

# Example usage
tracker = TokenTracker()

# Simulate token usage
tracker.log_tokens(100)
tracker.log_tokens(200)

print("Total Tokens Used:", tracker.total_tokens)
print("Estimated Cost:", tracker.calculate_cost())

# Optimizing prompts
prompt = "Explain the theory of relativity in simple terms."
optimized_prompt = "Simplify relativity theory."

print("Original Prompt:", prompt)
print("Optimized Prompt:", optimized_prompt)
