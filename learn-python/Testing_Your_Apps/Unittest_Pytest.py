# Unit Testing with unittest and pytest

# unittest example
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()

# pytest example
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
