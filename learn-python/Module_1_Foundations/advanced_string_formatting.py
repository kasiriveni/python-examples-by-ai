# Example: Advanced String Formatting
# Demonstrates alignment and padding in string formatting

# Left-align, right-align, and center-align
name = "AI"
print(f"|{name:<10}|")  # Left-align
print(f"|{name:>10}|")  # Right-align
print(f"|{name:^10}|")  # Center-align

# Padding with characters
print(f"|{name:-<10}|")  # Left-align with padding
print(f"|{name:*>10}|")  # Right-align with padding
print(f"|{name:=^10}|")  # Center-align with padding
