# AI Co-Pilot + Adoption Program 🚀

A production-ready prototype designed to accelerate daily tasks through Retrieval-Augmented Generation (RAG). This project is built as an end-to-end solution for knowledge management, meeting summarization, and automated drafting.

## 🎯 Project Vision

To empower employees with a secure, local AI assistant that enhances productivity while maintaining strict data governance and measurable KPIs.

## 🛠 Tech Stack

- **Backend:** FastAPI (Python 3.10)
- **LLM Engine:** Groq (Llama 3.3 70B) for ultra-fast inference.
- **Vector Database:** FAISS (Local Indexing).
- **Infrastructure:** Docker & Docker-Compose.
- **Telemetry:** Custom Python logging for KPI tracking (Latency, Status, User Feedback).

## 🚀 Quick Start (Local Deployment)

### Prerequisites

- Docker & Docker-Compose installed.
- A valid `GROQ_API_KEY`.

### Installation

1. **Clone the repo and create a `.env` file:**
   ```bash
   GROQ_API_KEY=your_key_here
   APP_PORT=8000
   ```
