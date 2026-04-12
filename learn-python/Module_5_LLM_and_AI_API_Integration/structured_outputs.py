# Example: Structured Outputs and JSON Mode
# Demonstrates generating structured outputs with OpenAI API

import openai
import json

openai.api_key = "your-api-key"

# Call the API
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Generate a JSON object with name, age, and profession.",
    max_tokens=50
)

# Parse the JSON output
output = response.choices[0].text.strip()
try:
    data = json.loads(output)
    print("Generated JSON:", data)
except json.JSONDecodeError:
    print("Failed to parse JSON:", output)
