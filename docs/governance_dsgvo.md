# KI-Governance & Datenschutz (DSGVO)

## 1. Safety Measures

- [cite_start]**PII Redaction**: All user input passes through a redaction layer to mask personal data before reaching the LLM API[cite: 160].
- [cite_start]**Data Minimization**: Only the most relevant text chunks (Top-K retrieval) are processed, reducing data exposure[cite: 159].

## 2. Risk Matrix

| Risk                   | Impact | Mitigation                                                                    |
| :--------------------- | :----- | :---------------------------------------------------------------------------- |
| **Data Leakage**       | High   | [cite_start]Local FAISS indexing; no training on user data[cite: 158].        |
| **Hallucinations**     | Medium | [cite_start]RAG-grounded responses with provenance (sources)[cite: 137, 158]. |
| **Inaccurate Results** | Low    | [cite_start]Continuous feedback loop (Thumbs Up/Down)[cite: 7, 139].          |

## 3. GDPR/DSGVO Checklist

- [x] **Transparency**: AI responses clearly labeled.
- [x] [cite_start]**Right to Erasure**: Local indices can be wiped instantly[cite: 162].
- [x] [cite_start]**Access Control**: Role-based access (RBAC) ready for Pilot phase[cite: 161].
