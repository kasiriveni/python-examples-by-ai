# Example: Prompt Engineering
# Demonstrates system prompts, few-shot learning, and chain-of-thought reasoning

import openai

openai.api_key = "your-api-key"

# System prompt
system_prompt = "You are a helpful assistant who explains Python code."

# Few-shot learning
few_shot_prompt = """
Explain the following Python code:

Code:
def add(a, b):
    return a + b

Explanation:
This function takes two arguments, `a` and `b`, and returns their sum.

Code:
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

Explanation:
"""

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"{system_prompt}\n{few_shot_prompt}",
    max_tokens=150
)

print(response.choices[0].text.strip())
