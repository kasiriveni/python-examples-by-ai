"""
This script demonstrates model serving with vLLM.
Topics covered:
1. Setting up a vLLM server.
2. Sending requests to the server.
"""

import requests

# Start the vLLM server (run this command in the terminal):
# vllm start --model gpt2

# Send a request to the vLLM server
url = "http://localhost:8000/generate"
payload = {
    "prompt": "What is the capital of France?",
    "max_tokens": 50
}
response = requests.post(url, json=payload)

print("Response from vLLM:", response.json())