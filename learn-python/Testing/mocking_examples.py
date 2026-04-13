"""
Mocking and patching in tests.
"""
from unittest.mock import Mock, patch, MagicMock, call
import json

# --- Code to test ---
class UserService:
    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def create_user(self, name, email):
        user = {"name": name, "email": email, "id": None}
        user["id"] = self.db.insert("users", user)
        self.email_service.send_welcome(email, name)
        return user

    def get_user(self, user_id):
        return self.db.find("users", user_id)

# --- Tests ---
def test_create_user_with_mock():
    """Using Mock objects to test UserService."""
    mock_db = Mock()
    mock_db.insert.return_value = 42

    mock_email = Mock()

    service = UserService(mock_db, mock_email)
    user = service.create_user("Alice", "alice@example.com")

    assert user["id"] == 42
    assert user["name"] == "Alice"

    mock_db.insert.assert_called_once_with("users", user)
    mock_email.send_welcome.assert_called_once_with("alice@example.com", "Alice")
    print("test_create_user_with_mock: PASSED")

def test_mock_return_values():
    """Configure mock return values."""
    mock = Mock()

    # Single return
    mock.method.return_value = 42
    assert mock.method() == 42

    # Side effects (multiple returns)
    mock.fetch.side_effect = [1, 2, 3]
    assert mock.fetch() == 1
    assert mock.fetch() == 2
    assert mock.fetch() == 3

    # Side effect as exception
    mock.fail.side_effect = ValueError("oops")
    try:
        mock.fail()
    except ValueError:
        pass

    print("test_mock_return_values: PASSED")

def test_mock_assertions():
    """Mock assertion methods."""
    mock = Mock()

    mock.process(1, 2, key="value")
    mock.process(3, 4)

    mock.process.assert_called()
    mock.process.assert_called_with(3, 4)
    assert mock.process.call_count == 2

    expected_calls = [
        call(1, 2, key="value"),
        call(3, 4),
    ]
    mock.process.assert_has_calls(expected_calls)
    print("test_mock_assertions: PASSED")

# Patching example
def fetch_data_from_api(url):
    """Function that would normally make HTTP requests."""
    import urllib.request
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

@patch('urllib.request.urlopen')
def test_fetch_data(mock_urlopen):
    """Patch urlopen to avoid real HTTP calls."""
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"name": "Alice", "age": 30}'
    mock_urlopen.return_value = mock_response

    result = fetch_data_from_api("https://api.example.com/user/1")

    assert result == {"name": "Alice", "age": 30}
    mock_urlopen.assert_called_once_with("https://api.example.com/user/1")
    print("test_fetch_data: PASSED")

if __name__ == "__main__":
    test_create_user_with_mock()
    test_mock_return_values()
    test_mock_assertions()
    test_fetch_data()
