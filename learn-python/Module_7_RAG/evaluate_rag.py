# Example: Evaluating RAG Pipelines
# Demonstrates how to evaluate RAG pipelines for relevance and faithfulness

from langchain.evaluation import Evaluator

# Example RAG pipeline output
retrieved_docs = ["LangChain is a framework for language models."]
generated_answer = "LangChain is a tool for AI applications."

# Evaluate relevance and faithfulness
evaluator = Evaluator()
relevance_score = evaluator.evaluate_relevance(retrieved_docs, generated_answer)
faithfulness_score = evaluator.evaluate_faithfulness(retrieved_docs, generated_answer)

print("Relevance Score:", relevance_score)
print("Faithfulness Score:", faithfulness_score)
