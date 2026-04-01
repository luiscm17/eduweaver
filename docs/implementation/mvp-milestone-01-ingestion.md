# MVP Milestone 01 — Document Ingestion Prototype

This milestone implements the **first functional core of the system**: the document ingestion pipeline.

The objective is to validate that a technical document can be:

1. Uploaded
2. Parsed
3. Converted into structured blocks
4. Chunked
5. Embedded
6. Indexed in the vector database

No UI or tutor interaction is required in this milestone. The goal is purely to validate the **knowledge pipeline**.

---

# 1. Milestone Goal

Create a working ingestion pipeline capable of transforming a PDF into retrievable chunks.

Expected pipeline:

```
PDF
 ↓
Parser
 ↓
ContentBlocks
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Database
```

Once completed, the system must support **manual retrieval queries** against the indexed document.

---

# 2. Scope

Included in this milestone:

- PDF ingestion
- parsing using Docling or Azure Document Intelligence
- normalization to Document Schema
- semantic chunking
- embedding generation
- vector indexing

Excluded from this milestone:

- frontend
- tutor service
- user authentication
- document library UI

---

# 3. Components Involved

Services used in this milestone:

- ingestion-service
- vector database
- blob storage

Relevant documentation:

- docs/dev/document-schema.md
- docs/dev/ingestion-pipeline.md
- docs/dev/retrieval-architecture.md

---

# 4. Implementation Tasks

## Task 1 — File Upload Simulation

Goal: simulate the ingestion entry point.

Steps:

- place a test PDF in a local folder or Blob Storage
- create a script that triggers the ingestion pipeline

Example test file:

```
docs/Artificial_Neural_Network_Model_for_Prediction_of_Drilling_Rate.md
```

---

## Task 2 — Parser Integration

Goal: extract structured data from the PDF.

Possible implementations:

- Docling parser
- Azure Document Intelligence

Expected output:

- headings
- paragraphs
- equations
- figures
- tables

---

## Task 3 — Normalization

Goal: convert parsed data into the **Normalized Document Schema**.

Output objects:

```
Document
Section
ContentBlock
```

Each block must include:

- block_type
- section_id
- content
- metadata

---

## Task 4 — Chunking

Goal: transform content blocks into semantic chunks suitable for RAG.

Rules:

- merge small paragraphs
- keep equations with explanation
- chunk size: 200–400 tokens

Output:

```
Chunk
  chunk_id
  document_id
  content
  metadata
```

---

## Task 5 — Embedding Generation

Goal: convert chunks into vector embeddings.

Possible models:

- Azure OpenAI embeddings
- OpenAI embeddings
- local embedding models

Each chunk must produce:

```
embedding_vector
```

---

## Task 6 — Vector Indexing

Goal: store embeddings in the vector database.

Possible databases:

- Azure AI Search
- Qdrant

Stored metadata must include:

- document_id
- section_title
- block_type
- page_number

---

## Task 7 — Retrieval Test

Goal: verify that relevant chunks can be retrieved.

Example test query:

```
"Explain the ROP equation"
```

Expected result:

- chunk containing the equation
- surrounding explanatory text

---

# 5. Acceptance Criteria

This milestone is considered complete when:

- A PDF can be ingested successfully
- ContentBlocks are generated
- Semantic chunks are created
- Embeddings are stored in the vector database
- Retrieval returns relevant chunks

---

# 6. Deliverables

Working components:

- ingestion-service prototype
- parsing integration
- chunking module
- embedding generation
- vector index integration

Artifacts produced:

- normalized_document.json
- chunks.json

---

# 7. Success Metric

The milestone is successful if:

- retrieval returns relevant technical context
- equations remain associated with their explanations
- chunks preserve document structure

Once this milestone works reliably, the next step is:

**MVP Milestone 02 — Retrieval + Tutor Integration**
