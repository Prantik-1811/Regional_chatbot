# Database Schema - Phase 1: HK Pilot

## Table: `cyber_knowledge_base`

| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | `UUID` | PK |
| `region` | `VARCHAR` | Default 'HK' |
| `source_url` | `TEXT` | |
| `title` | `TEXT` | |
| `content_block` | `TEXT` | |
| `embedding` | `VECTOR(1536)` | |
| `scraped_at` | `TIMESTAMPTZ` | |

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE cyber_knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region VARCHAR(10) DEFAULT 'HK',
    source_url TEXT NOT NULL,
    title TEXT NOT NULL,
    content_block TEXT NOT NULL,
    embedding VECTOR(1536),
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON cyber_knowledge_base USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON cyber_knowledge_base USING gin (content_block gin_trgm_ops);
```
