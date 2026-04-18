# Core Python Concepts

## Core Themes
- Unit testing with unittest and pytest styles.
- Mocking, patching, fixtures, and parameterized checks.
- Advanced assertion patterns and reusable test helpers.

## Core Theme Examples
- Example 1: Writing unittest.TestCase with assertEqual assertions.
- Example 2: Mocking external API calls with @patch decorator.
- Example 3: Using @pytest.mark.parametrize for multiple input checks.

## Files and Concepts
- advanced_testing.py: parameterized tests, assertions, custom test-runner helpers, data-structure testing
- mocking_examples.py: Mock, MagicMock, side_effect, patch decorators, call assertions
- pytest_examples.py: pytest parametrization, fixtures, raises checks, test classes
- testing_examples.py: unittest classes, pytest function-style tests
- unittest_example.py: unittest TestCase structure, patch-based mocking

## Core Example
This example uses unittest to verify a small helper function.

```python
import unittest

def add(left, right):
	return left + right

class AddTests(unittest.TestCase):
	def test_add(self):
		self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
	unittest.main()
```
