# Core Python Concepts

## Core Themes
- Calling LLM APIs and managing request patterns.
- Prompt engineering, streaming, and structured outputs.
- Token tracking, retry logic, and secure key management.

## Core Theme Examples
- Example 1: OpenAI API calls with message role structures.
- Example 2: Exponential backoff retry wrappers for API resilience.
- Example 3: Token counting with tiktoken for context management.

## Files and Concepts
- calling_openai_api.py: OpenAI-style API calls, model selection, token limits
- llm_api_patterns.py: message dataclasses, client wrappers, chat-completion patterns
- manage_api_keys.py: environment variables, dotenv, API secret handling
- multi_modal_inputs.py: image handling, multimodal request structure
- prompt_engineering.py: system prompts, few-shot prompting, chain-of-thought style prompting
- retry_logic.py: exponential backoff, retry wrappers for API resilience
- streaming_completions.py: streamed LLM outputs, chunk processing
- structured_outputs.py: JSON parsing, schema-like structured responses
- token_counting.py: tiktoken usage, token counting, context-window management

## Core Example
This example models a prompt as structured messages and counts words as a proxy for tokens.

```python
messages = [
	{"role": "system", "content": "You are helpful."},
	{"role": "user", "content": "Explain Python functions."},
]

token_estimate = sum(len(message["content"].split()) for message in messages)
reply = f"Estimated tokens: {token_estimate}"

print(reply)
```
