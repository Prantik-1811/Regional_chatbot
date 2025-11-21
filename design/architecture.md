# System Architecture - Phase 1: Hong Kong Pilot

## High-Level Flow
1.  **Scraper**: Python script using Scrapy to crawl `cybersecurity.hk`.
2.  **Database**: PostgreSQL with `pgvector` storing HK-only data.
3.  **Backend**: FastAPI serving a single RAG endpoint.
4.  **Frontend**: React app with a fixed Red theme for HK.

```mermaid
graph TD
    subgraph "HK Data Source"
        HK[Cyber Security Information Portal] -->|Scrapy| Raw[Raw HTML]
    end

    subgraph "Ingestion"
        Raw -->|Clean & Chunk| Chunks[Text Chunks]
        Chunks -->|Embed| Vectors[Embeddings]
        Vectors -->|Upsert| DB[(PostgreSQL)]
    end

    subgraph "Application"
        User -->|Query| UI[React UI (HK Theme)]
        UI -->|POST /query| API[FastAPI]
        API -->|Search| DB
        DB -->|Context| API
        API -->|Generate| LLM[LLM Service]
        LLM -->|Response| UI
    end
```
