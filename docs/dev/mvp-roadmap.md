# MVP Roadmap

This document defines the **Minimum Viable Product (MVP)** implementation plan for the AI Technical Reading Tutor.

The goal of the MVP is to validate the **core learning loop**:

1. User uploads a technical document
2. User reads the document
3. User asks questions
4. The AI tutor explains the content
5. The user continues learning

The MVP focuses on **core value** and intentionally avoids advanced features until the main workflow works reliably.

---

# 1. MVP Core Capabilities

The MVP will include the following features:

### 1. Document Upload

Users can upload technical documents.

Supported format for MVP:

- PDF

Future formats (post‑MVP):

- DOCX
- Markdown
- Web pages
- GitHub repositories

---

### 2. Document Processing

Uploaded PDFs are processed through the ingestion pipeline.

Pipeline steps:

1. Upload to Blob Storage
2. Trigger ingestion
3. Parse document
4. Generate ContentBlocks
5. Semantic chunking
6. Embeddings generation
7. Index chunks in vector database

Parser options:

- Azure Document Intelligence
- Docling

---

### 3. Document Viewer

Users can read the uploaded document inside the application.

Required capabilities:

- page navigation
- PDF rendering
- basic text selection

Suggested tool:

- PDF.js

---

### 4. AI Tutor Chat

Users can ask questions about the document.

Capabilities:

- question answering based on document context
- explanations in natural language
- support for explaining equations

Workflow:

User question
→ retrieval
→ prompt assembly
→ LLM response

---

### 5. Document‑Scoped Retrieval

The tutor retrieves context only from the **active document**.

Retrieval strategy:

- hybrid search (vector + keyword)
- section‑aware ranking
- structure‑aware chunks

This prevents mixing knowledge from unrelated documents.

---

### 6. Basic Library

Users can manage multiple uploaded documents.

Capabilities:

- list documents
- open document
- delete document

---

# 2. MVP Architecture

The MVP uses the architecture defined in `system-architecture.md`.

Components:

Frontend

- React / Next.js
- PDF viewer
- chat interface

Application API

- FastAPI
- document management
- authentication (optional for first prototype)

Tutor Service

- RAG retrieval
- prompt assembly
- LLM interaction

Knowledge Infrastructure

- Blob Storage
- Vector DB (Azure AI Search or Qdrant)

---

# 3. MVP Implementation Phases

The MVP should be implemented incrementally.

## Phase 1 — Document Ingestion

Goal: successfully ingest and index a document.

Tasks:

- upload PDF
- parse document
- generate chunks
- create embeddings
- store in vector index

Success criteria:

- chunks retrievable from index

---

## Phase 2 — Retrieval

Goal: verify that retrieval returns relevant document context.

Tasks:

- implement hybrid search
- document‑scoped filtering
- chunk ranking

Success criteria:

- retrieved chunks match expected sections

---

## Phase 3 — Tutor Integration

Goal: connect retrieval with an LLM.

Tasks:

- prompt assembly
- LLM response generation
- citations

Success criteria:

- correct explanations from document context

---

## Phase 4 — User Interface

Goal: enable real user interaction.

Tasks:

- PDF viewer
- chat interface
- document library

Success criteria:

- user can read and ask questions

---

# 4. Features Excluded from MVP

The following features are intentionally postponed.

Phase 2 features:

- DOCX ingestion
- web page ingestion
- repository ingestion
- advanced agentic retrieval
- prerequisite concept detection

Phase 3 features:

- exercise generation
- study mode
- collaborative annotations
- knowledge graphs
- math solver integration

These features will be added after validating the MVP.

---

# 5. Success Criteria

The MVP is considered successful if:

- Users can upload and read documents
- The tutor answers questions using document context
- Equation explanations work for common cases
- Retrieval accuracy is acceptable
- Response latency remains under 5 seconds

---

# 6. Summary

The MVP focuses on validating the **AI‑assisted reading experience**.

Core components:

- PDF ingestion
- document viewer
- RAG tutor
- document‑scoped retrieval
- user library

Once this workflow works reliably, the system can expand into a full **AI learning platform**.
