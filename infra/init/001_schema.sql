CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  filename TEXT NOT NULL,
  source_type VARCHAR(20) NOT NULL,
  content_hash TEXT UNIQUE NOT NULL,
  metadata JSONB DEFAULT '{}',
  status VARCHAR(20) DEFAULT 'processing',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chunks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID REFERENCES documents(id),
  content TEXT NOT NULL,
  embedding vector(1536),
  chunk_index INT,
  token_count INT,
  metadata JSONB DEFAULT '{}'
);

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (to_tsvector('english', content));