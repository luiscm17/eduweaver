# Repository Structure (Monorepo)

This document defines the **monorepo structure** for the project during the MVP stage.

The goal is to keep all services in a **single repository** while maintaining clear separation between components. This approach simplifies development, coordination, and versioning during the early stages of the project.

The repository contains four main parts:

- Frontend application
- Application API
- Tutor Service (AI layer)
- Ingestion pipeline

---

# 1. Why a Monorepo

Using a monorepo provides several advantages during early development.

Advantages:

- easier coordination between services
- shared types and utilities
- simpler dependency management
- single CI/CD pipeline
- easier refactoring across services

When the system grows significantly, the architecture may evolve into a **multi‑repo setup**, but that is not necessary for the MVP.

---

# 2. Top-Level Structure

Recommended repository structure:

```
eduweaver/

  apps/
    frontend/
    api/
    tutor-service/
    ingestion-service/

  packages/
    shared-types/
    prompt-templates/
    document-model/

  infrastructure/
    docker/
    terraform/
    scripts/

  docs/
    dev/
    architecture/

  tests/

  .github/
  README.md
```

---

# 3. Applications

All runnable services live inside `apps/`.

## frontend

Location:

```
apps/frontend/
```

Responsibilities:

- document viewer
- chat interface
- user library

Suggested stack:

- Next.js
- React
- PDF.js

---

## api

Location:

```
apps/api/
```

Responsibilities:

- authentication
- document library management
- file uploads
- reading progress
- forwarding chat queries to Tutor Service

Suggested stack:

- FastAPI
- PostgreSQL

---

## tutor-service

Location:

```
apps/tutor-service/
```

Responsibilities:

- retrieval logic
- prompt assembly
- LLM communication
- tool orchestration

Technologies:

- Python
- FastAPI
- LLM providers

This service implements the logic defined in:

```
docs/dev/retrieval-architecture.md
docs/dev/tutor-prompt-architecture.md
```

---

## ingestion-service

Location:

```
apps/ingestion-service/
```

Responsibilities:

- document parsing
- normalization
- content block generation
- chunking
- embedding creation
- vector indexing

Technologies:

- Python
- Azure Functions (or worker service)

Pipeline defined in:

```
docs/dev/ingestion-pipeline.md
```

---

# 4. Shared Packages

Reusable code lives in `packages/`.

This avoids duplication between services.

Example packages:

## shared-types

Shared data models:

- Document
- Section
- ContentBlock
- Chunk

These implement the schema defined in:

```
docs/dev/document-schema.md
```

---

## prompt-templates

Stores reusable prompt templates for the tutor.

Examples:

- equation explanation prompt
- code explanation prompt
- tutoring prompt

---

## document-model

Utilities for:

- converting parsed documents to NDF
- content block transformations
- chunk creation

---

# 5. Infrastructure

Infrastructure-related files live under `infrastructure/`.

Example structure:

```
infrastructure/
  docker/
  terraform/
  scripts/
```

This directory may contain:

- container definitions
- cloud deployment scripts
- environment setup

---

# 6. Documentation

Technical documentation lives in:

```
docs/dev/
```

Current architecture documents include:

- document-schema.md
- ingestion-pipeline.md
- retrieval-architecture.md
- tutor-prompt-architecture.md
- system-architecture.md
- mvp-roadmap.md

These documents define the **technical blueprint of the system**.

---

# 7. Testing

Tests are placed in:

```
tests/
```

Test categories may include:

- ingestion tests
- retrieval tests
- prompt tests
- integration tests

---

# 8. Future Migration to Multi‑Repo

If the system grows significantly, services may be split into separate repositories.

Possible future repositories:

- frontend
- application-api
- tutor-service
- ingestion-service

The monorepo structure ensures that this migration can occur gradually.

---

# 9. Summary

The monorepo structure organizes the project into clear domains:

- **apps/** for runnable services
- **packages/** for shared logic
- **infrastructure/** for deployment
- **docs/** for architecture

This structure keeps the project organized while allowing independent evolution of each component.
