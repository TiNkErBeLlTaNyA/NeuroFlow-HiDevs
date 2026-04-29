API Contracts — NeuroFlow

All APIs follow REST principles and use JSON for request/response bodies.
Authentication is assumed via JWT (Bearer Token) unless stated otherwise.

1. POST /ingest

Purpose: Ingest files or URLs into the system.

Request

{
  "source_type": "pdf | docx | image | csv | url",
  "source": "file_path_or_url",
  "metadata": {
    "tags": ["string"]
  }
}

Response

{
  "ingestion_id": "uuid",
  "status": "processing"
}

Errors

400 — Invalid input
413 — Payload too large

Auth: Required
Rate Limit: 10 requests/min

2. POST /query

Purpose: Execute RAG query.

Request

{
  "query": "string",
  "pipeline_id": "optional",
  "filters": {
    "tags": ["string"]
  }
}

Response

{
  "query_id": "uuid",
  "status": "processing"
}

Errors

400 — Invalid query
401 — Unauthorized

Auth: Required
Rate Limit: 30 requests/min

3. GET /query/{query_id}/stream

Purpose: Stream generated response (SSE).

Response (SSE events)

{ "token": "partial_text" }

Final event:

{
  "answer": "full_response",
  "sources": ["doc_ids"]
}

Errors

404 — Query not found

Auth: Required
Rate Limit: 50 connections/min

4. GET /evaluations

Purpose: Retrieve evaluation results (paginated).

Query Params

page
limit

Response

{
  "results": [
    {
      "query_id": "uuid",
      "faithfulness": 0.85,
      "relevance": 0.80
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10
  }
}

Errors

401 — Unauthorized

Auth: Required
Rate Limit: 20 requests/min

5. GET /evaluations/aggregate

Purpose: Get aggregated evaluation metrics.

Response

{
  "faithfulness_avg": 0.82,
  "relevance_avg": 0.79,
  "precision_avg": 0.75,
  "recall_avg": 0.77
}

Auth: Required
Rate Limit: 20 requests/min

6. POST /pipelines

Purpose: Create a pipeline configuration.

Request

{
  "name": "string",
  "retrieval_k": 10,
  "model": "model_name"
}

Response

{
  "pipeline_id": "uuid",
  "status": "created"
}

Auth: Required
Rate Limit: 10 requests/min

7. GET /pipelines/{id}/runs

Purpose: Retrieve pipeline execution history.

Response

{
  "runs": [
    {
      "run_id": "uuid",
      "status": "completed"
    }
  ]
}

Auth: Required
Rate Limit: 20 requests/min

8. POST /finetune/jobs

Purpose: Submit a fine-tuning job.

Request

{
  "dataset_id": "uuid",
  "base_model": "model_name"
}

Response

{
  "job_id": "uuid",
  "status": "submitted"
}

Auth: Required
Rate Limit: 5 requests/min

9. GET /finetune/jobs/{id}

Purpose: Get fine-tuning job status.

Response

{
  "status": "running | completed",
  "metrics": {
    "loss": 0.2
  }
}

Auth: Required
Rate Limit: 10 requests/min

10. GET /health

Purpose: Check system health.

Response

{
  "status": "ok"
}

Auth: Not required
Rate Limit: Unlimited

11. GET /metrics

Purpose: System metrics for monitoring.

Response

{
  "uptime": "string",
  "requests_per_min": 120
}

Auth: Not required
Rate Limit: Unlimited