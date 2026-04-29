## Context

NeuroFlow requires a vector database to store embeddings and perform similarity search. Options considered include pgvector, Pinecone, Weaviate, and Qdrant. The system also needs tight integration with metadata and cost efficiency.

## Decision

Use pgvector (PostgreSQL extension) as the primary vector store.

## Consequences

### Positive

Unified storage for vectors and metadata in a single database
Lower operational cost (no separate managed service required)
Easier integration with existing Postgres-based components

### Negative

Less scalable compared to dedicated vector databases at very large scale
Requires manual optimization for performance tuning