import csv
import os
import time
from datetime import datetime

# Path for the exportable metrics file
METRICS_FILE = "data/metrics.csv"

def log_interaction(query, latency_ms, status="success", feedback="N/A"):
    """
    Records interaction KPIs into a CSV file for stakeholder analysis.
    This fulfills the 'Exportable Metrics' requirement from the project blueprint.
    """
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    
    file_exists = os.path.isfile(METRICS_FILE)
    
    with open(METRICS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header definition based on the Adoption Program's KPI model
        if not file_exists:
            writer.writerow(["timestamp", "query", "latency_ms", "status", "feedback"])
        
        writer.writerow([
            datetime.now().isoformat(),
            query,
            round(latency_ms, 2),
            status,
            feedback if feedback else "N/A"
        ])

def generate_mock_data():
    """
    Generates synthetic data to simulate a week of usage for the stakeholder pitch.
    """
    import random
    sample_queries = [
        "How do I summarize meeting minutes?",
        "Explain the RAG architecture",
        "Generate a draft for a project status update",
        "What are the security risks of LLMs?"
    ]
    
    print(f"--- Generating Mock Telemetry Data ---")
    for _ in range(15):
        log_interaction(
            query=random.choice(sample_queries),
            latency_ms=random.uniform(450.0, 2500.0),
            status="success",
            feedback=random.choice(["thumbs_up", "thumbs_down", "N/A"])
        )
    print(f"✅ Data successfully written to {METRICS_FILE}")