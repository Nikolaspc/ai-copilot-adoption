# AI Governance & Risk Assessment

## 1. Data Privacy (DSGVO / GDPR Compliance)

- **Data Minimization:** The system only processes fragments of code/docs necessary for the specific query.
- **PII Redaction:** Users are instructed not to upload personal identifiable information. (Future Sprint: Auto-redaction layer).
- **Local Processing:** Embeddings and FAISS index are stored locally on the macOS environment, not in the cloud.
- **External Providers:** Groq API is used for inference. Data sent is subject to Groq's privacy policy (ensure no data retention for training).

## 2. Identified Risks & Mitigations

| Risk                 | Impact | Mitigation Strategy                                                  |
| :------------------- | :----- | :------------------------------------------------------------------- |
| **Hallucinations**   | High   | RAG integration ensures the model sticks to provided local context.  |
| **Data Leakage**     | Medium | Use of .env for API Keys and local FAISS storage.                    |
| **Prompt Injection** | Low    | Input sanitization at the FastAPI endpoint level.                    |
| **Model Bias**       | Low    | Use of Llama 3.3 (State-of-the-art) and expert-led prompt templates. |

## 3. Human-in-the-Loop

Every AI-generated draft (emails, summaries) must be reviewed by a human before being sent or published.
