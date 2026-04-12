"""
This script demonstrates tool/function calling with LLMs.
Topics covered:
1. Using an LLM to decide which tool to call.
2. Integrating Python functions as tools.
"""

from random import randint

# Define tools as Python functions
def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b

# Simulate an LLM deciding which tool to call
def llm_decision(prompt):
    if "add" in prompt:
        return "add_numbers"
    elif "multiply" in prompt:
        return "multiply_numbers"
    else:
        return "unknown"

# Main function to demonstrate tool calling
def main():
    prompt = "Please add two numbers."
    tool_name = llm_decision(prompt)

    if tool_name == "add_numbers":
        result = add_numbers(randint(1, 10), randint(1, 10))
    elif tool_name == "multiply_numbers":
        result = multiply_numbers(randint(1, 10), randint(1, 10))
    else:
        result = "No suitable tool found."

    print(f"Prompt: {prompt}")
    print(f"Tool Used: {tool_name}")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
