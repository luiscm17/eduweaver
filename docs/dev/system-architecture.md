# System Architecture

This document describes the **high‑level architecture** of the AI Technical Reading Tutor system. The architecture separates application logic from AI reasoning components to achieve **scalability, modularity, and maintainability**.

The system is composed of five primary layers:

1. Frontend (User Interface)
2. Application API
3. Tutor Service (AI Layer)
4. Document Ingestion Pipeline
5. Knowledge Infrastructure

This separation ensures that traditional backend responsibilities remain isolated from AI workloads such as retrieval, prompting, and LLM orchestration.

---

# 1. Architecture Overview

High‑level system flow:

```
Frontend (React / Next.js)
        │
        ▼
Application API (FastAPI)
        │
        ├── Document Storage (Azure Blob Storage)
        │
        ├── Database (Postgres)
        │
        ▼
Tutor Service (AI Service)
        │
        ├── Vector Database (Azure AI Search / Qdrant)
        │
        └── LLM Providers
             ├─ Azure OpenAI
             ├─ OpenAI
             └─ Local Models (Ollama)

Background Processing:

Blob Storage Trigger
        ▼
Ingestion Pipeline
        ▼
Document Parsing → Chunking → Embeddings → Indexing
```

---

# 2. Frontend Layer

The frontend provides the user interface for interacting with documents and the AI tutor.

Suggested stack:

- React or Next.js
- PDF.js viewer

Core UI components:

- Document viewer
- Chat sidebar
- Text selection tools
- Reading progress tracking

Primary responsibilities:

- render documents
- send questions to backend
- display tutor responses
- manage user session

---

# 3. Application API

The Application API manages **business logic and user data**.

Suggested technology:

- FastAPI

Responsibilities:

- authentication
- document library management
- file uploads
- reading progress
- permissions

Example endpoints:

```
POST /documents/upload
GET /documents
GET /documents/{id}
POST /reading-progress
POST /chat/query
```

The `/chat/query` endpoint forwards user questions to the **Tutor Service**.

Important rule:

The Application API **does not execute RAG or LLM logic**.

---

# 4. Tutor Service (AI Layer)

The Tutor Service is responsible for **AI reasoning and retrieval**.

Suggested technology:

- Python
- FastAPI

Responsibilities:

- retrieval from vector index
- prompt assembly
- LLM interaction
- optional tool execution

Example endpoint:

```
POST /tutor/query
```

Example request payload:

```
{
  "user_id": "123",
  "document_id": "abc",
  "question": "Explain the equation",
  "selected_text": "...",
  "page": 12
}
```

Response example:

```
{
  "answer": "...",
  "citations": [...],
  "sources": [...]
}
```

The Tutor Service internally executes:

1. Retrieval
2. Prompt construction
3. LLM reasoning
4. Response generation

---

# 5. Document Ingestion Pipeline

Documents are processed asynchronously after upload.

Trigger architecture:

```
User Upload
      │
      ▼
Azure Blob Storage
      │
Blob Event Trigger
      │
Azure Function
      │
Ingestion Pipeline
```

Pipeline steps:

1. Source detection
2. Parsing
3. Normalization
4. Content block generation
5. Chunking
6. Embedding generation
7. Vector indexing

Supported sources:

- PDF
- DOCX
- Markdown
- GitHub repositories
- Web pages

---

# 6. Knowledge Infrastructure

The knowledge infrastructure stores document assets and indexed information.

Components:

### Blob Storage

Stores:

- original documents
- extracted images
- processed artifacts

Example structure:

```
documents/
  {document_id}/
      original/
      images/
      processed/
```

### Vector Database

Stores document chunks and embeddings.

Supported systems:

- Azure AI Search
- Qdrant

Each chunk includes metadata:

- document_id
- section_title
- page_number
- block_type

---

# 7. Retrieval Flow

The typical question flow is:

```
User Question
      │
Frontend
      │
Application API
      │
Tutor Service
      │
Vector Search
      │
Context Assembly
      │
LLM Response
      │
Frontend
```

Retrieval is always **filtered by document_id** to prevent mixing context from unrelated documents.

---

# 8. Scalability Strategy

Separating the Tutor Service enables independent scaling.

Example scenario:

```
Application API instances: 2
Tutor Service instances: 8
```

This architecture allows AI workloads to scale without affecting application infrastructure.

---

# 9. Deployment Model

Initial deployment can use simple container services.

Possible environments:

- Azure Container Apps
- Docker containers
- Virtual machines

Advanced orchestration (e.g., Kubernetes) can be introduced later if needed.

---

# 10. Future Extensions

Potential future components:

- math solver service
- code execution sandbox
- knowledge graph service
- study plan generator
- collaborative annotation service

Because the Tutor Service is isolated, these features can be added without modifying the Application API.

---

# 11. Summary

The architecture separates the system into two major domains:

Application Layer

- user management
- document storage
- application logic

AI Layer

- retrieval
- reasoning
- tutoring

This separation allows the system to evolve from a simple document assistant into a **full AI learning platform** without architectural redesign.
