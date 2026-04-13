"""
Regular expressions with strings in Python.
"""
import re

text = "Contact us at support@example.com or sales@company.org"

# Basic matching
pattern = r'\b[\w.+-]+@[\w-]+\.[\w.]+\b'
emails = re.findall(pattern, text)
print(f"Emails found: {emails}")

# Match vs Search
result = re.match(r'\d+', "123abc")
print(f"Match at start: {result.group() if result else None}")

result = re.search(r'\d+', "abc123def")
print(f"Search anywhere: {result.group() if result else None}")

# Groups
date_text = "Born on 2024-03-15"
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_text)
if match:
    print(f"Year: {match.group(1)}, Month: {match.group(2)}, Day: {match.group(3)}")

# Named groups
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
match = re.search(pattern, date_text)
if match:
    print(f"Named: {match.groupdict()}")

# Substitution
cleaned = re.sub(r'\s+', ' ', "Hello    World   Python")
print(f"Cleaned: '{cleaned}'")

censored = re.sub(r'\b(bad|ugly)\b', '***', "This is a bad ugly day", flags=re.IGNORECASE)
print(f"Censored: {censored}")

# Split
parts = re.split(r'[,;|]+', "apple,banana;cherry|date,,fig")
print(f"Split: {parts}")

# Compiled patterns (better performance for repeated use)
phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
phones = phone_pattern.findall("Call 555-123-4567 or 555.987.6543")
print(f"Phones: {phones}")

# Lookahead and lookbehind
text = "price: $100, discount: $20, total: $80"
prices = re.findall(r'(?<=\$)\d+', text)
print(f"Prices: {prices}")

# Non-greedy matching
html = "<b>bold</b> and <i>italic</i>"
greedy = re.findall(r'<.*>', html)
non_greedy = re.findall(r'<.*?>', html)
print(f"Greedy: {greedy}")
print(f"Non-greedy: {non_greedy}")

# Flags
result = re.findall(r'python', "Python PYTHON python", re.IGNORECASE)
print(f"Case insensitive: {result}")

# Multiline
text = """Line 1
Line 2
Line 3"""
starts = re.findall(r'^Line \d', text, re.MULTILINE)
print(f"Lines starting with 'Line': {starts}")
