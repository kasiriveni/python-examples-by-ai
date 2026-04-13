"""
Exception groups and ExceptionGroup (Python 3.11+).
"""

# ExceptionGroup for handling multiple errors at once
def validate_form(data):
    errors = []
    if not data.get("name"):
        errors.append(ValueError("Name is required"))
    if not data.get("email"):
        errors.append(ValueError("Email is required"))
    if data.get("age") and data["age"] < 0:
        errors.append(ValueError("Age must be positive"))
    if errors:
        raise ExceptionGroup("Validation failed", errors)

# Handling ExceptionGroup with except*
try:
    validate_form({"age": -5})
except* ValueError as eg:
    for err in eg.exceptions:
        print(f"Validation error: {err}")

# Nested exception groups
def process_batch(items):
    errors = []
    results = []
    for i, item in enumerate(items):
        try:
            if item < 0:
                raise ValueError(f"Negative value at index {i}: {item}")
            results.append(item ** 2)
        except ValueError as e:
            errors.append(e)
    if errors:
        raise ExceptionGroup("Batch processing errors", errors)
    return results

try:
    process_batch([1, -2, 3, -4, 5])
except* ValueError as eg:
    print(f"\n{len(eg.exceptions)} errors in batch:")
    for err in eg.exceptions:
        print(f"  - {err}")

# Notes and add_note (Python 3.11+)
try:
    x = int("not_a_number")
except ValueError as e:
    e.add_note("This occurred while parsing user input")
    e.add_note("Input was received from form field 'quantity'")
    try:
        raise
    except ValueError as e2:
        print(f"Exception: {e2}")
        for note in e2.__notes__:
            print(f"  Note: {note}")
