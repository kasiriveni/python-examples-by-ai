"""
This script demonstrates LLM observability using LangSmith, Langfuse, and Helicone.
Topics covered:
1. Logging LLM interactions.
2. Observing and analyzing LLM behavior.
"""

# Example: Logging with LangSmith
class LangSmithLogger:
    def log_interaction(self, prompt, response):
        print(f"LangSmith Log - Prompt: {prompt}, Response: {response}")

# Example: Logging with Langfuse
class LangfuseLogger:
    def log_interaction(self, prompt, response):
        print(f"Langfuse Log - Prompt: {prompt}, Response: {response}")

# Example: Logging with Helicone
class HeliconeLogger:
    def log_interaction(self, prompt, response):
        print(f"Helicone Log - Prompt: {prompt}, Response: {response}")

# Example usage
prompt = "What is the capital of France?"
response = "The capital of France is Paris."

langsmith_logger = LangSmithLogger()
langfuse_logger = LangfuseLogger()
helicone_logger = HeliconeLogger()

langsmith_logger.log_interaction(prompt, response)
langfuse_logger.log_interaction(prompt, response)
helicone_logger.log_interaction(prompt, response)
