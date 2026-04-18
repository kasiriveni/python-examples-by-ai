# Core Python Concepts

## Core Themes
- Different layers of application testing.
- Framework-specific tests, integration tests, and browser-driven checks.
- Comparing unittest, pytest, doctest, and nose workflows.

## Core Theme Examples
- Example 1: Unit test for business logic and Flask test client for endpoints.
- Example 2: Using Selenium to automate browser interactions and assertions.
- Example 3: Running doctests from docstrings with pytest discovery.

## Files and Concepts
- Doctest.py: doctest in docstrings, embedded executable examples
- Functional_Testing.py: Selenium browser automation, element selection, functional checks
- Integration_Testing.py: Flask test client, HTTP method testing, response validation
- Nose.py: nose test discovery and execution conventions
- pytest_patterns.py: setup_method, parametrized tests, service and business-logic checks
- Unittest_Pytest.py: unittest versus pytest comparison, test organization patterns

## Core Example
This example shows a doctest and a plain assertion in the same module.

```python
def total(values):
	"""
	>>> total([1, 2, 3])
	6
	"""
	return sum(values)

def test_total():
	assert total([4, 5]) == 9
```
