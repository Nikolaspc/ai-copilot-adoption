import os
import requests
import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings for Groq API.
    Fastest inference engine for RAG applications.
    """
    groq_api_key: str = os.getenv("GROQ_API_KEY", "missing_key")
    # Using Llama 3.3 70B for high-quality reasoning
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

    def _detect_intent(self, prompt: str):
        """
        Internal logic to switch system prompts based on user intent.
        Addresses requirements: RAG, Summarization, and Action Item Extraction.
        """
        query = prompt.lower()
        
        # Default RAG / Chat intent
        system_instruction = (
            "You are a Senior AI Lead. Use the provided context to answer "
            "the question concisely and professionally."
        )
        temperature = 0.2

        # Summarization intent
        if any(word in query for word in ["summar", "resum", "recap"]):
            system_instruction = (
                "You are an Executive Assistant. Create a structured summary "
                "of the provided text using bullet points for key topics."
            )
            temperature = 0.5  # Slightly higher for better prose
        
        # Action Items intent
        elif any(word in query for word in ["action", "task", "todo", "tarea"]):
            system_instruction = (
                "You are a Project Manager. Extract a clear list of actionable items, "
                "deadlines, and owners from the text. Use a checkbox format."
            )
            temperature = 0.1 # Very focused and literal

        return system_instruction, temperature

    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Orchestrates the LLM request with dynamic system prompts.
        """
        if self.api_key == "missing_key":
            return "Configuration Error: Check your .env file."
        
        system_msg, temp = self._detect_intent(prompt)
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": system_msg
                    },
                    {
                        "role": "user", 
                        "content": f"Context provided: {prompt}\n\nPlease process the input accordingly."
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temp
            }

            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                data=json.dumps(payload),
                timeout=25
            )
            
            if response.status_code != 200:
                return f"Groq API Error {response.status_code}: {response.text}"
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            return f"Network Error (Groq): {str(e)}"