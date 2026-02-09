# KI-Governance & Datenschutz (DSGVO)

## 1. Local-First Approach

Die Verarbeitung erfolgt primär lokal auf macOS-Infrastruktur. Dies minimiert das Risiko von Datenabfluss an Drittanbieter.

## 2. Risikomatrix

| Risiko              | Auswirkung | Mitigierung                                                            |
| :------------------ | :--------- | :--------------------------------------------------------------------- |
| **Datenschutz**     | Hoch       | Einsatz von PII-Redaction (Anonymisierung) vor jeder LLM-Verarbeitung. |
| **Halluzinationen** | Mittel     | RAG-Einsatz: Antworten sind durch lokale Dokumente (FAISS) belegt.     |
| **Sicherheit**      | Hoch       | Keine externe API-Abhängigkeit im Standardmodus (Air-gapped möglich).  |

## 3. DSGVO Checklist

- [x] Datenminimierung: Nur relevante Textfragmente werden verarbeitet.
- [x] Transparenz: Alle KI-Antworten werden als solche gekennzeichnet.
- [x] Recht auf Löschung: Lokale Indizes (FAISS) können jederzeit gelöscht werden.
