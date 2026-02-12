# AI Co-Pilot + Adoption Program 🚀

A production-ready prototype designed to accelerate daily tasks through Retrieval-Augmented Generation (RAG). This project is built as an end-to-end solution for knowledge management, meeting summarization, and automated drafting.

## 🎯 Project Vision

To empower employees with a secure AI assistant that enhances productivity while maintaining strict data governance and providing measurable business KPIs.

## 🌟 Key Features

- **Knowledge-Based RAG:** Queries local documents via FAISS vector database.
- **Intelligent Intent Detection:** Automatic switching between **Chat**, **Meeting Summarization**, and **Action Item Extraction**.
- **Production Telemetry:** Real-time logging of latency, token usage, and user feedback (stored in `data/metrics.csv`).
- **Governance-Ready:** Modular architecture designed for DSGVO/GDPR compliance.

## 🛠 Tech Stack

- **Backend:** FastAPI (Python 3.10)
- **LLM Engine:** Groq (Llama 3.3 70B - Versatile)
- **Vector DB:** FAISS (Local)
- **Telemetry:** Custom Python CSV Logger
- **CI/CD:** GitHub Actions (Linting & Unit Testing)

## 🚀 Quick Start (Local Deployment)

### Prerequisites

- Docker & Docker-Compose installed.
- A valid `GROQ_API_KEY`.

### Installation & Run

1. **Prepare Environment:**
   Create a `.env` file in the root directory:
   ```bash
   GROQ_API_KEY=your_key_here
   APP_PORT=8000
   Launch with Docker:
   ```

Bash
docker-compose up --build
The API will be available at http://localhost:8000. Access /docs for Swagger UI.

🧪 Testing & Quality Assurance
We follow a strict CI/CD pipeline. To run the unit tests locally:

Bash

# Set up a local environment

python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
pip install pytest

# Execute tests

PYTHONPATH=. pytest tests/
Tests cover: Intent detection logic, API key error handling, and RAG flow.

📊 Telemetry & KPIs
The system automatically tracks every interaction. You can export the performance data for stakeholders:

Location: data/metrics.csv

Key Metrics: Request Latency, Intent Accuracy, and User Feedback (Thumbs Up/Down).

🛡 Governance & Privacy
Data Locality: Vector indexes are stored locally.

Minimization: Only relevant document chunks are sent to the LLM.

Audit Trail: Every response is logged with a unique Request ID for traceability.

📂 Project Structure
Plaintext
├── .github/workflows/ # CI/CD Pipelines
├── app/
│ ├── core/ # LLM Logic & Vector DB
│ ├── api/ # FastAPI Endpoints
│ └── main.py # Entry point
├── data/ # Vector Index & Metrics
├── docs/ # Architecture & Governance docs
├── tests/ # Unit & Integration tests
└── Dockerfile # Containerization
