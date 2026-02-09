from llama_cpp import Llama
import os

class LLMAdapter:
    def __init__(self, model_path="models/tinyllama.gguf"):
        # Explicit check for the model file
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        # Optimization for older Macs: Force CPU only
        self.llm = Llama(
            model_path=model_path,
            n_ctx=512,      # Context window
            n_threads=4,    # Number of CPU cores to use
            n_gpu_layers=0, # <--- CRITICAL: Set to 0 to disable Metal/GPU
            verbose=False
        )

    def generate_response(self, prompt: str, max_tokens: int = 100) -> str:
        # Chat format for TinyLlama
        formatted_prompt = f"<|system|>\nUse the context to answer.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
        
        output = self.llm(
            formatted_prompt,
            max_tokens=max_tokens,
            stop=["</s>"],
            echo=False
        )
        
        return output["choices"][0]["text"].strip()