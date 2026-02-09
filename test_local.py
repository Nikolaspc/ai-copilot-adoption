from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Define a small, efficient model (DeepSeek-1.5B)
model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

print("Loading model into RAM... (this might take a few minutes)")

try:
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.float32, # Standard precision for CPU compatibility
        device_map="cpu"           # Strictly use CPU
    )

    print("--- Local AI Ready (Transformers Mode) ---")

    # Simple prompt
    prompt = "User: What is 2+2?\nAssistant:"
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate answer
    outputs = model.generate(**inputs, max_new_tokens=20)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Response:\n{answer}")

except Exception as e:
    print(f"An error occurred: {e}")