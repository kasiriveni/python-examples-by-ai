# Example: Managing API Keys Securely
# Demonstrates how to use python-dotenv and environment variables

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("API key not found. Please set OPENAI_API_KEY in your .env file.")

print("API key loaded successfully.")
