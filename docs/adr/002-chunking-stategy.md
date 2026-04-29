## Context

Chunking directly impacts retrieval quality. Options include:

Fixed-size chunking
Sentence-boundary chunking
Semantic chunking

Each approach has trade-offs between simplicity and contextual coherence.

## Decision

Use a hybrid approach:

Default: semantic chunking (for better context preservation)
Fallback: fixed-size chunking (when semantic parsing is unreliable or expensive)

## Consequences

### Positive

Improved retrieval quality due to meaningful context grouping
Flexibility to handle different document types

### Negative

Increased preprocessing complexity
Slightly higher computational cost during ingestion