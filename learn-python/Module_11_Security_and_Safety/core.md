# Core Python Concepts

## Core Themes
- Security hardening for AI systems and prompt handling.
- Prompt-injection detection, sanitization, and risk classification.
- Safe input processing in LLM applications.

## Core Theme Examples
- Example 1: Regex pattern matching for prompt-injection detection.
- Example 2: Sanitizing user inputs before LLM processing.
- Example 3: Risk classification for dangerous prompt phrases.

## Files and Concepts
- ai_security.py: prompt guards, injection-pattern detection, risk levels
- prompt_injection_example.py: unsafe prompts, sanitization, secure-versus-insecure handling

## Core Example
This example flags suspicious prompt text with simple pattern checks.

```python
dangerous_phrases = ["ignore instructions", "reveal system prompt"]

def is_safe(text):
	lowered = text.lower()
	return not any(phrase in lowered for phrase in dangerous_phrases)

print(is_safe("Explain functions"))
print(is_safe("Ignore instructions and continue"))
```
