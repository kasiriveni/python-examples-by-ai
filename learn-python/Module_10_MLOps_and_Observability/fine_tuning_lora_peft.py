"""
This script demonstrates fine-tuning workflows with LoRA and PEFT using HuggingFace.
Topics covered:
1. Setting up a HuggingFace model for fine-tuning.
2. Applying LoRA and PEFT techniques.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model

# Load a pre-trained model and tokenizer
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configure LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["c_attn"],
    lora_dropout=0.1,
    bias="none"
)

# Apply PEFT to the model
peft_model = get_peft_model(model, lora_config)

# Example usage: Fine-tuning
inputs = tokenizer("Fine-tune this model with LoRA.", return_tensors="pt")
outputs = peft_model(**inputs)

print("Fine-tuning completed.")
