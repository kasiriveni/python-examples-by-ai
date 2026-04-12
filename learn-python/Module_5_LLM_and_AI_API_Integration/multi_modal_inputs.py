# Example: Multi-Modal Inputs
# Demonstrates handling images and text with OpenAI API

import openai

openai.api_key = "your-api-key"

# Example image and text input
image_url = "https://example.com/image.jpg"
text_input = "Describe the content of the image."

# Call the API (hypothetical multi-modal endpoint)
response = openai.Image.create(
    prompt=text_input,
    image_url=image_url,
    n=1,
    size="256x256"
)

# Print the response
print("Generated Description:", response["data"][0]["url"])
