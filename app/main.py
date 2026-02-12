from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import time

# Internal imports
try:
    from app.core.rag_engine import RAGEngine
    from app.core.llm_adapter import LLMAdapter
    from app.core.telemetry import log_interaction
except ImportError:
    from core.rag_engine import RAGEngine
    from core.llm_adapter import LLMAdapter
    from core.telemetry import log_interaction

app = FastAPI(
    title="AI Co-Pilot Adoption API",
    description="RAG-powered Assistant with Telemetry & Memory",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query: str
    feedback: str # "thumbs_up" or "thumbs_down"

# Global state
rag_engine = None
llm_adapter = None
chat_history = [] 

@app.on_event("startup")
async def startup_event():
    global rag_engine, llm_adapter
    print("\n--- 🚀 Starting AI Co-Pilot Server (Sprint 3: Telemetry) ---")
    try:
        rag_engine = RAGEngine()
        print("✅ FAISS Index loaded.")
    except Exception as e:
        print(f"⚠️ FAISS Warning: {e}")
    llm_adapter = LLMAdapter()
    print("✅ LLM Adapter ready.")

@app.get("/")
async def root():
    return {"status": "online", "metrics_endpoint": "/api/metrics"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global chat_history
    if not rag_engine or not llm_adapter:
        raise HTTPException(status_code=503, detail="System not ready.")

    start_time = time.time()
    
    # 1. Retrieval
    context = rag_engine.search(request.query, k=2)

    # 2. Memory & Prompt Construction
    recent_history = "\n".join(chat_history[-4:])
    combined_prompt = f"Context:\n{context}\n\nHistory:\n{recent_history}\n\nUser: {request.query}"

    # 3. Generation
    answer = llm_adapter.generate_response(combined_prompt)
    
    # 4. Telemetry (KPI: Latency)
    latency_ms = (time.time() - start_time) * 1000
    log_interaction(request.query, latency_ms, status="success") # [cite: 8, 154]
    
    # 5. History Update
    chat_history.append(f"User: {request.query}")
    chat_history.append(f"AI: {answer}")
    
    return {
        "response": answer,
        "latency_ms": round(latency_ms, 2)
    }

@app.get("/api/metrics")
async def get_metrics():
    """Export KPIs to CSV for stakeholders."""
    file_path = "data/metrics.csv"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/csv', filename="kpi_metrics.csv")
    raise HTTPException(status_code=404, detail="No metrics found yet.")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)