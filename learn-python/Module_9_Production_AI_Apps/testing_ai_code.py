"""
This script demonstrates testing AI code with pytest and mocking.
Topics covered:
1. Writing unit tests with pytest.
2. Mocking LLM calls.
3. Snapshot testing.
"""

import pytest
from unittest.mock import patch

# Example function to test
def call_llm(prompt):
    # Simulate an LLM call (e.g., OpenAI API)
    return f"Response to: {prompt}"

# Test cases
@pytest.mark.parametrize("prompt,expected", [
    ("Hello", "Response to: Hello"),
    ("Test", "Response to: Test"),
])
def test_call_llm(prompt, expected):
    assert call_llm(prompt) == expected

@patch("__main__.call_llm", return_value="Mocked response")
def test_mock_llm(mock_call):
    response = call_llm("Ignored prompt")
    assert response == "Mocked response"

# Snapshot testing
@pytest.fixture
def snapshot():
    return {"prompt": "Hello", "response": "Response to: Hello"}

def test_snapshot(snapshot):
    assert snapshot == {"prompt": "Hello", "response": "Response to: Hello"}