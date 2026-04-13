"""
Example of using docstrings and type hints for better code documentation.
"""
def greet(name: str) -> str:
    """
    Greets the user with their name.

    Args:
        name (str): The name of the user.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("Alice"))
