from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime
import csv

app = FastAPI(title="AI Co-Pilot API")

class QueryRequest(BaseModel):
    user_id: str
    query: str

class FeedbackRequest(BaseModel):
    query_id: str
    rating: int
    comment: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

@app.post("/api/query")
async def process_query(request: QueryRequest):
    return {
        "query_id": "req-123",
        "answer": "This is a placeholder response for the RAG flow.",
        "provenance": ["doc_1.pdf", "doc_2.txt"]
    }

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    return {"status": "success", "message": "Feedback received"}

@app.get("/api/metrics")
async def export_metrics():
    return {"download_url": "/metrics/export.csv"}