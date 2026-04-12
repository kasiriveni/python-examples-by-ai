# Example: Token Counting and Context Window Management
# Demonstrates how to count tokens and manage context windows

import tiktoken

# Load the tokenizer for the OpenAI model
tokenizer = tiktoken.get_encoding("cl100k_base")

# Example prompt
prompt = "Write a Python function to calculate the factorial of a number."

# Count tokens
tokens = tokenizer.encode(prompt)
print(f"Number of tokens: {len(tokens)}")

# Manage context window
max_tokens = 4096
if len(tokens) > max_tokens:
    print("Prompt exceeds the maximum context window size.")
