# Integration Testing

from flask import Flask
import unittest

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Integration Testing!"

# /post api

@app.route('/post', methods=['POST'])
def post():
    return "Post request received!"




class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Hello, Integration Testing!")

if __name__ == '__main__':
    unittest.main()
