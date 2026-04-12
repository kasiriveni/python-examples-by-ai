# Example: Streaming Completions
# Demonstrates handling streaming responses with OpenAI API

import openai

openai.api_key = "your-api-key"

# Call the API with streaming enabled
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Write a Python function to calculate Fibonacci numbers.",
    max_tokens=100,
    stream=True
)

# Process the streaming response
for chunk in response:
    if "choices" in chunk:
        print(chunk["choices"][0]["text"], end="")
