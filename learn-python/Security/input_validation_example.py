"""
Example of validating user input for security.
"""
def validate_username(username):
    if not username.isalnum():
        raise ValueError("Username must be alphanumeric.")
    if len(username) < 5:
        raise ValueError("Username must be at least 5 characters long.")
    return True

if __name__ == "__main__":
    try:
        username = input("Enter a username: ")
        if validate_username(username):
            print("Username is valid.")
    except ValueError as e:
        print(f"Invalid username: {e}")
