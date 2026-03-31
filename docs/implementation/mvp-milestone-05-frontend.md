# MVP Milestone 05 — Frontend MVP

This milestone introduces the **first user-facing interface** of the system. It connects the previously built backend components into a usable application where a user can upload, read, and ask questions about technical documents.

This milestone builds on:

- **Milestone 01 — Document Ingestion** (documents parsed and indexed)
- **Milestone 02 — Retrieval Layer** (relevant chunks retrieved)
- **Milestone 03 — Tutor Service** (RAG explanations working)
- **Milestone 04 — Application API** (backend endpoints available)

The goal of this milestone is to validate the **core learning experience**:

```
Upload → Read → Ask → Learn
```

---

# 1. Milestone Goal

Deliver a minimal frontend application that allows users to:

- upload documents
- browse their document library
- read a document
- ask the AI tutor questions

Expected interaction flow:

```
User
 ↓
Frontend UI
 ↓
Application API
 ↓
Tutor Service
 ↓
RAG + LLM
```

---

# 2. Scope

Included in this milestone:

- document upload UI
- document library view
- PDF reader
- tutor chat sidebar
- integration with Application API

Excluded from this milestone:

- advanced UI design
- authentication system
- collaborative features
- annotation tools

---

# 3. Components Involved

Applications involved:

- `apps/frontend`
- `apps/api`
- `apps/tutor-service`

Relevant documentation:

- docs/dev/system-architecture.md
- docs/dev/repo-layout-tree.md

---

# 4. Implementation Tasks

## Task 1 — Frontend Application Setup

Create the frontend project.

Suggested stack:

- Next.js
- React
- TypeScript

Suggested location:

```
apps/frontend/
```

Basic structure:

```
app/
components/
lib/
styles/
```

---

## Task 2 — Document Upload UI

Create a simple interface for uploading documents.

Interaction:

```
Select file
 ↓
Upload
 ↓
POST /documents/upload
```

After upload, the document appears in the library.

---

## Task 3 — Document Library

Display the list of uploaded documents.

API used:

```
GET /documents
```

UI features:

- document title
- upload date
- open document button

---

## Task 4 — Document Reader

Implement a document viewer.

Recommended tool:

```
PDF.js
```

Capabilities:

- page navigation
- zoom
- text selection

---

## Task 5 — Tutor Chat Sidebar

Add a chat panel next to the document reader.

Features:

- message input
- conversation history
- AI responses

API used:

```
POST /chat/query
```

Example request:

```
{
  "document_id": "doc_123",
  "question": "Explain this equation"
}
```

---

## Task 6 — Text Selection Support (Optional)

Allow users to copy or send selected text to the tutor.

Example interaction:

```
User selects equation
 ↓
"Ask Tutor"
 ↓
Selected text included in query
```

---

# 5. Acceptance Criteria

This milestone is complete when:

- users can upload a document
- documents appear in the library
- documents can be opened in the reader
- users can ask tutor questions
- tutor responses appear in the chat

---

# 6. Deliverables

Working components:

- frontend application
- document upload interface
- document library
- PDF reader
- tutor chat

---

# 7. Success Metric

The MVP is considered successful if a user can complete the full learning loop:

```
1. Upload a technical document
2. Open the document
3. Ask questions
4. Receive explanations from the tutor
```

This validates the **core product hypothesis** of an AI‑assisted scientific reading experience.

---

# 8. MVP Completion

After this milestone the system will support:

- document ingestion
- structured knowledge indexing
- retrieval‑augmented tutoring
- application backend
- user interface

At this point the **Minimum Viable Product is complete** and ready for early testing.
