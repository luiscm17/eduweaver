# MVP Milestone 02 — Retrieval Layer

This milestone implements the **document retrieval layer** used by the tutor system. The objective is to verify that the system can reliably retrieve relevant context from indexed documents before integrating the LLM.

This milestone builds directly on **Milestone 01 — Document Ingestion**, which produced:

- normalized document structure
- semantic chunks
- vector embeddings
- indexed content in the vector database

The focus of this stage is to ensure that **queries return the correct technical context** from the document.

---

# 1. Milestone Goal

Create a working retrieval layer capable of locating relevant information inside a document using hybrid search.

Expected pipeline:

```
User Question
 ↓
Query Processing
 ↓
Vector Search
 ↓
Keyword Search
 ↓
Ranking
 ↓
Relevant Chunks
```

The milestone is complete when retrieval returns **correct document context** for typical technical questions.

---

# 2. Scope

Included in this milestone:

- retrieval queries against the vector database
- hybrid search implementation
- document‑scoped filtering
- chunk ranking
- retrieval test scripts

Excluded from this milestone:

- LLM integration
- tutor prompts
- frontend UI
- API integration

---

# 3. Components Involved

Services used in this milestone:

- tutor-service (retrieval module only)
- vector database

Relevant documentation:

- docs/dev/retrieval-architecture.md
- docs/dev/document-schema.md
- docs/dev/ingestion-pipeline.md

---

# 4. Implementation Tasks

## Task 1 — Retrieval Module

Create the base retrieval module inside the tutor service.

Suggested location:

```
apps/tutor-service/app/retrieval/
```

Core files:

```
vector_search.py
ranking.py
query_processor.py
```

Responsibilities:

- process queries
- execute vector search
- execute keyword search
- combine results

---

## Task 2 — Vector Search

Goal: retrieve semantically similar chunks using embeddings.

Steps:

1. generate embedding from user query
2. query vector database
3. retrieve top‑k chunks

Example query:

```
"Explain the ROP equation"
```

Expected result:

- chunk containing the equation
- surrounding explanatory text

---

## Task 3 — Keyword Search

Goal: complement vector search with exact matches.

Keyword search is useful for technical terms such as:

- variable names
- formula symbols
- domain‑specific terminology

Example terms:

```
ROP
WOB
gradient descent
```

---

## Task 4 — Document‑Scoped Filtering

Goal: ensure retrieval only searches inside the active document.

Required filter:

```
document_id = current_document
```

This prevents mixing context from different documents.

---

## Task 5 — Chunk Ranking

Goal: rank retrieved chunks to prioritize the most useful context.

Ranking signals may include:

- vector similarity score
- keyword match score
- section proximity
- chunk type priority

Example chunk priority:

| Chunk Type | Priority |
|------------|----------|
| equation | high |
| code | high |
| paragraph | medium |
| figure | medium |
| table | medium |

---

## Task 6 — Retrieval Test Script

Goal: validate retrieval quality using test queries.

Create a script that executes retrieval without using an LLM.

Example test queries:

```
Explain the ROP model
What does the equation R = K (W/db)^as N^e mean?
What variables affect drilling rate?
```

The script should output:

- retrieved chunks
- section title
- similarity score

---

# 5. Acceptance Criteria

This milestone is complete when:

- vector search retrieves relevant chunks
- keyword search retrieves technical matches
- hybrid search improves retrieval accuracy
- retrieval respects document scope
- top results contain correct technical context

---

# 6. Deliverables

Working components:

- retrieval module
- vector search implementation
- keyword search implementation
- chunk ranking system
- retrieval test scripts

---

# 7. Success Metric

The milestone is successful if:

- relevant chunks appear in the top results
- equation explanations retrieve both the formula and context
- retrieval latency remains under ~300 ms

Once retrieval is validated, the next milestone is:

**MVP Milestone 03 — Tutor Service Integration**
