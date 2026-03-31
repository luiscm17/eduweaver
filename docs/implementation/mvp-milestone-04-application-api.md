# MVP Milestone 04 — Application API

This milestone introduces the **Application API**, the backend responsible for managing users, documents, and coordinating requests between the frontend and the Tutor Service.

It builds on previous milestones:

- **Milestone 01 — Ingestion** (documents parsed and indexed)
- **Milestone 02 — Retrieval** (relevant chunks retrievable)
- **Milestone 03 — Tutor Service** (RAG explanations working)

The goal of this milestone is to expose a **real backend interface** that a client application can use.

---

# 1. Milestone Goal

Provide a backend API that allows clients to:

- upload documents
- list and open documents
- ask questions to the tutor
- store basic reading progress

Expected request flow:

```
Client
  ↓
Application API
  ↓
Tutor Service
  ↓
Vector DB + LLM
```

---

# 2. Scope

Included in this milestone:

- FastAPI backend
- document upload endpoint
- document listing
- tutor query endpoint
- integration with Tutor Service

Excluded from this milestone:

- production authentication
- advanced permissions
- UI integration

---

# 3. Components Involved

Services used in this milestone:

- `apps/api`
- `apps/tutor-service`
- Blob Storage
- Vector DB

Relevant documentation:

- docs/dev/system-architecture.md
- docs/dev/repo-structure.md
- docs/dev/repo-layout-tree.md

---

# 4. Implementation Tasks

## Task 1 — API Skeleton

Create the base FastAPI application.

Suggested location:

```
apps/api/app/main.py
```

Example structure:

```
app/
  main.py
  routers/
  services/
  models/
```

---

## Task 2 — Document Upload Endpoint

Endpoint:

```
POST /documents/upload
```

Responsibilities:

- receive PDF
- store file in Blob Storage
- register document metadata
- trigger ingestion pipeline

---

## Task 3 — Document Library

Endpoints:

```
GET /documents
GET /documents/{document_id}
DELETE /documents/{document_id}
```

These endpoints allow users to manage their document library.

---

## Task 4 — Tutor Query Endpoint

Endpoint:

```
POST /chat/query
```

Example request:

```
{
  "document_id": "doc_123",
  "question": "Explain the ROP equation",
  "selected_text": "R = K (W/db)^as N^e"
}
```

The API forwards the request to the **Tutor Service**.

---

## Task 5 — Tutor Service Integration

The Application API should communicate with the Tutor Service via HTTP.

Example internal call:

```
POST /tutor/query
```

The response is then returned to the client.

---

## Task 6 — Reading Progress (Basic)

Optional lightweight endpoint:

```
POST /reading-progress
```

Stores:

- document_id
- page
- timestamp

This enables the reader to resume where they left off.

---

# 5. Acceptance Criteria

This milestone is complete when:

- documents can be uploaded
- ingestion pipeline is triggered
- documents appear in the library
- tutor queries work through the API

---

# 6. Deliverables

Working components:

- FastAPI backend
- document endpoints
- tutor query endpoint
- integration with Tutor Service

---

# 7. Success Metric

The milestone is successful if a client can perform the full flow:

```
upload document
   ↓
document indexed
   ↓
ask question
   ↓
receive tutor explanation
```

Once validated, the next milestone is:

**MVP Milestone 05 — Frontend Interface**
