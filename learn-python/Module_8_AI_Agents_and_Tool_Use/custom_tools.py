"""
This script demonstrates building custom tools for LLMs.
Topics covered:
1. Creating Python functions as tools.
2. Wrapping tools with metadata for LLM integration.
"""

# Define custom tools
def greet_user(name):
    return f"Hello, {name}!"

def calculate_square(number):
    return number ** 2

# Wrap tools with metadata
tools = {
    "greet_user": {
        "function": greet_user,
        "description": "Greets the user by name."
    },
    "calculate_square": {
        "function": calculate_square,
        "description": "Calculates the square of a number."
    }
}

# Simulate an LLM calling a tool
def call_tool(tool_name, *args):
    if tool_name in tools:
        tool = tools[tool_name]["function"]
        return tool(*args)
    else:
        return "Tool not found."

# Example usage
print(call_tool("greet_user", "Alice"))
print(call_tool("calculate_square", 4))
