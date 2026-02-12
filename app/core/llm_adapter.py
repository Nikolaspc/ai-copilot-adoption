import os
import requests
import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings for Groq API.
    Fastest inference engine for RAG.
    """
    groq_api_key: str = os.getenv("GROQ_API_KEY", "missing_key")
    # Llama 3.3 70B es un modelo de élite disponible gratis en Groq
    model_name: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = ".env"

settings = Settings()

class LLMAdapter:
    def __init__(self):
        print("--- Initializing Groq Adapter (Professional Tier) ---")
        self.api_key = settings.groq_api_key
        self.model = settings.model_name
        
        if self.api_key == "missing_key" or not self.api_key:
            print("❌ Error: GROQ_API_KEY not found in .env!")
        else:
            print(f"✅ Groq Engine Ready (Model: {self.model})")

    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        if self.api_key == "missing_key":
            return "Configuration Error: Check your .env file."
        
        try:
            # Groq API uses the same format as OpenAI
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a Senior AI Lead. Use the provided context to answer the question concisely and professionally."
                    },
                    {
                        "role": "user", 
                        "content": f"Context from FAISS: {prompt}\n\nQuestion: Based on the context, what is the status and goal of the project?"
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.2
            }

            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                data=json.dumps(payload),
                timeout=20
            )
            
            if response.status_code != 200:
                return f"Groq API Error {response.status_code}: {response.text}"
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            return f"Network Error (Groq): {str(e)}"