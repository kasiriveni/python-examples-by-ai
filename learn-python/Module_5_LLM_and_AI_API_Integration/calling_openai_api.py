# Example: Calling OpenAI API
# Demonstrates how to call the OpenAI API for text completion

import openai

# Set your API key
openai.api_key = "your-api-key"

# Call the API
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Write a Python function to calculate factorial.",
    max_tokens=100
)

# Print the response
print(response.choices[0].text.strip())