System Architecture — NeuroFlow

NeuroFlow is a multi-modal LLM orchestration platform consisting of five core subsystems: Ingestion, Retrieval, Generation, Evaluation, and Fine-Tuning. Each subsystem is responsible for a specific stage in the data and model lifecycle.

1. Ingestion Subsystem

Purpose
Transforms raw input data into vector representations for retrieval.

Supported Inputs
PDF, DOCX, images, CSV, and web URLs.

Data Flow

User Upload (/ingest)
→ Content Extraction (based on file type)
→ Text Cleaning
→ Chunking
→ Embedding Generation
→ Vector Store (pgvector)
→ Metadata Store (Postgres)

2. Retrieval Subsystem

Purpose
Fetches relevant context for a user query using hybrid retrieval.

Pipeline

User Query
→ Query Embedding
→ Parallel:
   → Vector Similarity Search
   → Keyword Search (BM25)
   → Metadata Filtering
→ Reciprocal Rank Fusion
→ Cross-Encoder Re-ranking
→ Top-K Context Window

3. Generation Subsystem

Purpose
Generates responses using retrieved context and appropriate LLM routing.

Flow

Context Window
→ Prompt Construction
→ Model Routing (cost / capability / domain)
→ LLM Inference
→ Token Streaming (SSE)
→ Logging (input + output)

4. Evaluation Subsystem

Purpose
Evaluates response quality asynchronously using automated metrics.

Pipeline

Generated Response + Context
→ Async Evaluation
→ LLM-as-Judge Scoring
→ Metrics Calculation
→ Store in Postgres
→ Rolling Aggregation

Metrics

Faithfulness
Answer Relevance
Context Precision
Context Recall

5. Fine-Tuning Subsystem

Purpose
Improves model performance using high-quality interactions.

Selection Criteria

Faithfulness > 0.8
User Rating ≥ 4

Pipeline

Evaluation Logs
→ Filter High-Quality Data
→ Convert to JSONL
→ Fine-Tuning Job Submission
→ Track via MLflow
→ Model Registry Update
→ Routing to Improved Model