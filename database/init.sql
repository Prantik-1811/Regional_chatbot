-- Enable Extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Main Knowledge Base Table
CREATE TABLE IF NOT EXISTS cyber_knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region VARCHAR(10) DEFAULT 'HK',
    source_url TEXT NOT NULL,
    title TEXT NOT NULL,
    content_block TEXT NOT NULL,
    embedding VECTOR(1536),
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_ckb_embedding ON cyber_knowledge_base 
USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_ckb_content_trgm ON cyber_knowledge_base 
USING gin (content_block gin_trgm_ops);
