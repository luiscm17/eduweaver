# Initial Monorepo File Layout (MVP)

This document shows the **initial file and directory layout** for the project monorepo during the MVP stage.

The goal is to provide a **clear starting structure** so development can begin without reorganizing the repository later.

The layout separates:

- user-facing applications
- backend services
- AI services
- ingestion pipeline
- shared packages
- infrastructure

---

# 1. Repository Tree

```
eduweaver/

├─ apps/
│
│  ├─ frontend/
│  │  ├─ app/
│  │  ├─ components/
│  │  │  ├─ document-viewer/
│  │  │  ├─ chat/
│  │  │  └─ library/
│  │  ├─ lib/
│  │  ├─ styles/
│  │  ├─ public/
│  │  └─ package.json
│
│  ├─ api/
│  │  ├─ app/
│  │  │  ├─ routers/
│  │  │  │  ├─ documents.py
│  │  │  │  ├─ library.py
│  │  │  │  └─ chat.py
│  │  │  ├─ services/
│  │  │  │  ├─ document_service.py
│  │  │  │  └─ storage_service.py
│  │  │  ├─ models/
│  │  │  ├─ config/
│  │  │  └─ main.py
│  │  ├─ tests/
│  │  └─ pyproject.toml
│
│  ├─ tutor-service/
│  │  ├─ app/
│  │  │  ├─ retrieval/
│  │  │  │  ├─ vector_search.py
│  │  │  │  └─ ranking.py
│  │  │  ├─ prompts/
│  │  │  │  ├─ tutor_prompt.py
│  │  │  │  └─ equation_prompt.py
│  │  │  ├─ tools/
│  │  │  │  ├─ retrieve_document_context.py
│  │  │  │  └─ retrieve_equation_context.py
│  │  │  ├─ providers/
│  │  │  │  ├─ openai_provider.py
│  │  │  │  └─ azure_provider.py
│  │  │  └─ main.py
│  │  ├─ tests/
│  │  └─ pyproject.toml
│
│  └─ ingestion-service/
│     ├─ app/
│     │  ├─ adapters/
│     │  │  ├─ blob_storage.py
│     │  │  ├─ parser_adapters.py
│     │  ├─ config/
│     │  │  ├─ settings.py
│     │  │  └─ credentials.py
│     │  ├─ pipeline/
│     │  │  ├─ azure_ai_search/
│     │  │  │  ├─ knowledge_base.py
│     │  │  │  ├─ knowledge_source.py
│     │  │  │  └─ mcp_connection.py
│     │  │  ├─ docling/
│     │  │  ├─ normalize.py
│     │  │  ├─ chunking.py
│     │  │  └─ embeddings.py
│     │  ├─ indexing/
│     │  │  └─ vector_indexer.py
│     │  └─ main.py
│     └─ pyproject.toml

├─ packages/
│
│  ├─ document-model/
│  │  ├─ document.py
│  │  ├─ section.py
│  │  ├─ content_block.py
│  │  └─ chunk.py
│
│  ├─ prompt-templates/
│  │  ├─ tutoring_prompt.md
│  │  ├─ equation_prompt.md
│  │  └─ code_explanation_prompt.md
│
│  └─ shared-types/
│     ├─ document_types.py
│     └─ api_types.py

├─ infrastructure/
│  ├─ docker/
│  │  ├─ api.Dockerfile
│  │  ├─ tutor.Dockerfile
│  │  └─ ingestion.Dockerfile
│  ├─ scripts/
│  │  ├─ start-dev.sh
│  │  └─ ingest-test.sh
│  └─ terraform/

├─ tests/
│  ├─ ingestion/
│  ├─ retrieval/
│  └─ tutor/

├─ docs/
│  └─ dev/
│     ├─ document-schema.md
│     ├─ ingestion-pipeline.md
│     ├─ retrieval-architecture.md
│     ├─ tutor-prompt-architecture.md
│     ├─ system-architecture.md
│     ├─ mvp-roadmap.md
│     ├─ repo-structure.md
│     └─ repo-layout-tree.md

├─ .github/
│  └─ workflows/
│     └─ ci.yml

├─ README.md
└─ .gitignore
```

---

# 2. Development Workflow

Typical local development flow:

```
1. Start API service
2. Start Tutor Service
3. Run ingestion worker
4. Run frontend
```

Example development commands:

```
pnpm dev:frontend
python apps/api/app/main.py
python apps/tutor-service/app/main.py
python apps/ingestion-service/app/main.py
```

---

# 3. Design Principles

This layout follows several principles:

Separation of concerns

- apps → runnable services
- packages → reusable logic
- infrastructure → deployment
- docs → architecture and design

Independent services

Each service can run independently during development.

Shared domain model

The `document-model` package ensures that all services use the same data structures.

---

# 4. Summary

This repository layout enables:

- clean separation between services
- easy local development
- scalable architecture
- shared domain models

The structure supports the **monorepo strategy for the MVP** while remaining compatible with a future multi‑repository architecture if the project grows.
