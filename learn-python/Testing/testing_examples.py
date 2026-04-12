# Testing examples: unittest and pytest style
# unittest example
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2,3), 5)

# pytest style (same functions work with pytest)
def test_add_pytest():
    assert add(1,2) == 3

if __name__ == '__main__':
    unittest.main()
