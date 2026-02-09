import torch
from transformers import pipeline
import sys

print("--- System Diagnostics ---")
print(f"Python version: {sys.version.split()[0]}")
print(f"PyTorch version: {torch.__version__}")

try:
    print("\nLoading TinyLlama (1.1B)... this is a very compatible model.")
    # This model is around 700MB, much lighter for your RAM
    pipe = pipeline(
        "text-generation", 
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
        torch_dtype=torch.float32, 
        device_map="cpu"
    )

    print("\n✅ Success! Local AI is active.")
    
    prompt = "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nWhat is 2+2?</s>\n<|assistant|>\n"
    
    outputs = pipe(prompt, max_new_tokens=20, do_sample=True, temperature=0.7)
    print(f"\nResponse: {outputs[0]['generated_text'].split('<|assistant|>')[-1].strip()}")

except Exception as e:
    print(f"\n❌ Error during execution: {e}")