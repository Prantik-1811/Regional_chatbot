# RAG Pipeline - HK Pilot

## Logic
1.  **Input**: User query.
2.  **Filter**: `region = 'HK'` (Implicit).
3.  **Search**:
    -   Embed query.
    -   Cosine similarity search in `cyber_knowledge_base`.
    -   Top 5 results.
4.  **Guardrail**:
    -   If max score < 0.75 -> Return "No relevant HK government data found."
5.  **Generate**:
    -   Prompt: "Answer using only this HK context..."
    -   Cite sources.
