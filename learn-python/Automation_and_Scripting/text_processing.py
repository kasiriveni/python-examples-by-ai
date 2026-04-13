"""
Automation: Text processing and regex.
"""
import re
from collections import Counter

# Log parsing
sample_log = """
2024-03-15 10:23:45 INFO  Server started on port 8080
2024-03-15 10:24:01 ERROR Database connection failed: timeout
2024-03-15 10:24:15 WARN  Retrying database connection
2024-03-15 10:24:20 INFO  Database connected successfully
2024-03-15 10:25:00 ERROR Authentication failed for user admin
2024-03-15 10:25:30 INFO  User alice logged in
2024-03-15 10:26:00 DEBUG Processing request /api/users
2024-03-15 10:26:05 ERROR Internal server error: NullPointerException
"""

# Extract all error messages
errors = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ERROR\s+(.*)', sample_log)
print("Errors found:")
for error in errors:
    print(f"  - {error}")

# Count log levels
levels = re.findall(r'(INFO|ERROR|WARN|DEBUG)', sample_log)
level_counts = Counter(levels)
print(f"\nLog level counts: {dict(level_counts)}")

# Extract timestamps
timestamps = re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', sample_log)
print(f"Time range: {timestamps[0]} to {timestamps[-1]}")

# Text replacement pipeline
def clean_text(text):
    """Clean and normalize text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Normalize case
    text = text.lower()
    return text

messy = "  Hello,   WORLD!!!  This   is   a    TEST...  @#$%  "
print(f"\nCleaned: '{clean_text(messy)}'")

# Data extraction from semi-structured text
invoice = """
Invoice #12345
Date: 2024-03-15
Customer: Acme Corp

Items:
  Widget A    x5    $10.99
  Widget B    x3    $24.50
  Service C   x1    $199.00

Total: $353.45
"""

invoice_num = re.search(r'Invoice #(\d+)', invoice).group(1)
items = re.findall(r'\s+(\w[\w\s]+?)\s+x(\d+)\s+\$([0-9.]+)', invoice)
total = re.search(r'Total: \$([0-9.]+)', invoice).group(1)

print(f"\nInvoice #{invoice_num}")
for name, qty, price in items:
    print(f"  {name.strip()}: {qty} x ${price}")
print(f"Total: ${total}")

# Word frequency analysis
text = """Python is a powerful programming language. Python is used for web development,
data science, automation, and more. Python's simplicity makes it a great choice
for beginners and experts alike."""

words = re.findall(r'\b\w+\b', text.lower())
freq = Counter(words).most_common(10)
print("\nTop 10 words:")
for word, count in freq:
    print(f"  {word}: {count}")
