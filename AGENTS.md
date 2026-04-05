# AGENTS.md

Guidelines for autonomous coding agents working in this repository.
This file explains how to build, run, test, and modify the project safely.

The project is a **Python monorepo managed with `uv`** and currently contains
an ingestion service used for document processing and indexing.

---

# Repository Overview

Project: **eduweaver**

Directory structure (simplified):

```
apps/
  ingestion_service/
    app/
      main.py
      adapters/
      indexing/
      pipeline/
      config/
```

Pipeline stages follow a transformation model:

```
parse → normalize → chunk → embed → index
```

Key responsibilities:

- **pipeline/** – document transformation stages
- **indexing/** – vector index creation and updates
- **adapters/** – external integrations (blob storage, search, etc.)
- **config/** – environment and runtime configuration

Agents should preserve this layered architecture.

---

# Environment Setup

The project uses **uv** for dependency management.

Python requirement:

```
>=3.13
```

Install dependencies:

```
uv sync
```

Create environment (if needed):

```
uv venv
```

Run commands inside the environment:

```
uv run <command>
```

---

# Running the Service

Primary entrypoint:

```
apps/ingestion_service/app/main.py
```

Run ingestion on a document:

```
uv run python -m apps.ingestion_service.app.main <file>
```

Prefer **module execution (`-m`)** instead of executing files directly.

---

# Build Commands

There is no compilation step.

Build = dependency resolution.

```
uv sync
```

Optional packaging (future):

```
uv build
```

---

# Linting & Formatting

Linting is handled with **Ruff**.

Run linter:

```
uv run ruff check .
```

Auto‑fix lint issues:

```
uv run ruff check . --fix
```

Format code:

```
uv run ruff format .
```

Agents should run formatting before committing changes.

---

# Testing

Testing framework: **pytest** (expected convention).

Run all tests:

```
uv run pytest
```

Run a single file:

```
uv run pytest tests/test_pipeline.py
```

Run a single test:

```
uv run pytest tests/test_pipeline.py::test_chunk_document
```

Run tests matching a pattern:

```
uv run pytest -k chunk
```

Agents introducing new functionality should add tests when possible.

---

# Code Style

## General Principles

- Prefer clarity over cleverness
- Keep functions small and composable
- Avoid hidden side effects
- Favor pure transformations in pipeline stages

---

# Imports

Use **absolute imports** from the repository root.

Example:

```
from apps.ingestion_service.app.pipeline.chunk_document import chunk_document
```

Avoid relative imports.

Import order:

1. Standard library
2. Third‑party libraries
3. Local modules

---

# Formatting Rules

- 4 space indentation
- 88–100 column width
- trailing commas in multiline structures
- use double quotes for strings

Example:

```
result = process_document(
    text,
    chunk_size=512,
)
```

---

# Type Hints

All new code should include **Python type hints**.

Example:

```
def chunk_document(text: str, chunk_size: int) -> list[str]:
```

Prefer built‑in generics:

```
list[str]
dict[str, Any]
```

Avoid `Any` unless necessary.

---

# Naming Conventions

Variables and functions:

```
snake_case
```

Classes:

```
PascalCase
```

Constants:

```
UPPER_SNAKE_CASE
```

Files:

```
snake_case.py
```

---

# Error Handling

Never swallow exceptions.

Bad:

```
except Exception:
    pass
```

Good:

```
except Exception as exc:
    raise RuntimeError("Pipeline stage failed") from exc
```

Errors should provide meaningful context.

---

# Logging

Prefer structured logging instead of prints.

Example:

```
import logging

logger = logging.getLogger(__name__)
logger.info("Processing document", extra={"chunks": len(chunks)})
```

`print()` is acceptable only for CLI feedback.

---

# Architecture Guidelines

Pipeline modules should follow:

```
input → transform → output
```

Each stage should:

- accept explicit inputs
- return explicit outputs
- avoid global state

Avoid circular imports between pipeline stages.

---

# Files Agents Must Never Modify

Do not modify generated or environment folders:

```
.venv/
.ruff_cache/
.git/
__pycache__/
```

---

# Editor / AI Rules

No Cursor rules (`.cursor/rules`) or Copilot rules
(`.github/copilot-instructions.md`) were detected in this repository.

If they are introduced later, agents must follow them in addition
to this document.
