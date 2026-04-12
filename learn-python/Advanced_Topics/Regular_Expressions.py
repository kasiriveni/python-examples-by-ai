# Regular Expressions

import re

# Match example
pattern = r"\d+"
text = "The number is 42."
match = re.search(pattern, text)
if match:
    print("Found:", match.group())
