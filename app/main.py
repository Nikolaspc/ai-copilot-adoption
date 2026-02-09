from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# Internal imports
from app.utils.redactor import PIIRedactor
from app.core.llm_adapter import LLMAdapter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI(title="AI Co-Pilot API")

# --- CORS Configuration ---
# This allows your frontend (port 3000) to talk to your backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components once to optimize memory on your Mac
redactor = PIIRedactor()
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Ensure TinyLlama is ready via PyTorch 2.2.2
llm = LLMAdapter()

class QueryRequest(BaseModel):
    user_id: str
    query: str

@app.get("/health")
def health_check():
    """Service health check endpoint."""
    return {"status": "healthy", "model": "TinyLlama-1.1B"}

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """
    Main RAG endpoint:
    1. Redacts PII
    2. Searches FAISS for context
    3. Generates response using Local LLM
    """
    # 1. Privacy Filter
    clean_query = redactor.redact(request.query)
    
    index_path = "data/faiss_index"
    if not os.path.exists(index_path):
        return {
            "query_id": "error",
            "answer": "Knowledge base not indexed yet. Please run ingest.py first.",
            "provenance": []
        }

    try:
        # 2. Retrieval (RAG)
        vectorstore = FAISS.load_local(
            index_path, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        # Search for the top 3 relevant chunks
        docs = vectorstore.similarity_search(clean_query, k=3)
        context_text = " ".join([d.page_content for d in docs])
        sources = list(set([d.metadata.get('source', 'unknown') for d in docs]))
        
        # 3. Generation (Local LLM)
        # We build a prompt that forces the AI to use the retrieved context
        refined_prompt = f"Context: {context_text}\n\nQuestion: {clean_query}\n\nAnswer:"
        ai_response = llm.generate_response(refined_prompt)
        
        return {
            "query_id": "req-local-rag",
            "answer": ai_response,
            "provenance": sources
        }
        
    except Exception as e:
        print(f"Error during RAG flow: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during generation.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)