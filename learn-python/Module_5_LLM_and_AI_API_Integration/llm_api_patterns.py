"""
Module 5: LLM and AI API Integration patterns.
"""
import json
import os
import time
from dataclasses import dataclass, field
from typing import Optional

# === API Client Pattern ===
@dataclass
class Message:
    role: str  # "system", "user", "assistant"
    content: str

@dataclass
class ChatCompletion:
    model: str
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 1000

    def to_dict(self):
        return {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in self.messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

class LLMClient:
    """Simulated LLM API client demonstrating the pattern."""

    def __init__(self, api_key=None, base_url="https://api.openai.com/v1"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "demo-key")
        self.base_url = base_url
        self.request_count = 0

    def chat(self, messages, model="gpt-4", **kwargs):
        """Send chat completion request."""
        self.request_count += 1
        completion = ChatCompletion(
            model=model,
            messages=[Message(**m) if isinstance(m, dict) else m for m in messages],
            **kwargs
        )
        # In real code, this would make an HTTP request
        print(f"  [API] Request #{self.request_count}: {completion.model}")
        print(f"  [API] Messages: {len(completion.messages)}")
        return {
            "id": f"chatcmpl-{self.request_count}",
            "choices": [{"message": {"role": "assistant", "content": "Simulated response"}}],
            "usage": {"prompt_tokens": 50, "completion_tokens": 30, "total_tokens": 80},
        }

# === Prompt Templates ===
print("=== Prompt Templates ===")

class PromptTemplate:
    def __init__(self, template, **defaults):
        self.template = template
        self.defaults = defaults

    def format(self, **kwargs):
        params = {**self.defaults, **kwargs}
        return self.template.format(**params)

# Define reusable templates
SUMMARIZE = PromptTemplate(
    "Summarize the following {format} in {length} words:\n\n{text}",
    format="text",
    length="100"
)

CLASSIFY = PromptTemplate(
    "Classify the following text into one of these categories: {categories}\n\nText: {text}\n\nCategory:",
)

CODE_REVIEW = PromptTemplate(
    "Review this {language} code for bugs, security issues, and improvements:\n\n```{language}\n{code}\n```",
    language="python"
)

# Use templates
print(SUMMARIZE.format(text="Python is a versatile programming language..."))
print()
print(CLASSIFY.format(
    categories="positive, negative, neutral",
    text="This product is amazing!"
))

# === Conversation Memory ===
print("\n=== Conversation Memory ===")

class ConversationMemory:
    def __init__(self, system_prompt="You are a helpful assistant.", max_messages=20):
        self.system_prompt = system_prompt
        self.messages = []
        self.max_messages = max_messages

    def add_user_message(self, content):
        self.messages.append(Message("user", content))
        self._trim()

    def add_assistant_message(self, content):
        self.messages.append(Message("assistant", content))
        self._trim()

    def get_messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            *[{"role": m.role, "content": m.content} for m in self.messages],
        ]

    def _trim(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def clear(self):
        self.messages = []

memory = ConversationMemory("You are a Python tutor.")
memory.add_user_message("What is a decorator?")
memory.add_assistant_message("A decorator is a function that wraps another function...")
memory.add_user_message("Can you show an example?")

print(f"Messages in memory: {len(memory.messages)}")
for msg in memory.get_messages():
    print(f"  [{msg['role']}] {msg['content'][:50]}...")

# === Token Counting (simplified) ===
print("\n=== Token Estimation ===")

def estimate_tokens(text):
    """Rough token estimation (~4 chars per token for English)."""
    return len(text) // 4

def estimate_cost(prompt_tokens, completion_tokens, model="gpt-4"):
    prices = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    }
    p = prices.get(model, prices["gpt-4"])
    return (prompt_tokens * p["input"] + completion_tokens * p["output"]) / 1000

text = "This is a sample prompt for token estimation."
tokens = estimate_tokens(text)
cost = estimate_cost(tokens, 100, "gpt-4")
print(f"Text: '{text}'")
print(f"Estimated tokens: {tokens}")
print(f"Estimated cost: ${cost:.4f}")

# === Retry with backoff ===
print("\n=== API Client Demo ===")
client = LLMClient()
response = client.chat([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain Python decorators"},
])
print(f"  Response ID: {response['id']}")
print(f"  Usage: {response['usage']}")
