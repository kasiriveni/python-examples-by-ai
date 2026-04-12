# Example: Retry Logic and Exponential Backoff
# Demonstrates how to implement retry logic with exponential backoff

import openai
import time

openai.api_key = "your-api-key"

def call_openai_with_retries(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100
            )
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    raise Exception("All retry attempts failed.")

# Example usage
try:
    result = call_openai_with_retries("Write a Python function to calculate Fibonacci numbers.")
    print(result)
except Exception as e:
    print(e)
