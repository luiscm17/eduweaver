# AGENTS.md

This document provides guidance for autonomous coding agents operating in this repository.
It explains how to build, run, test, and modify the codebase safely and consistently.

The repository is a Python project managed with **uv** and structured as a small monorepo
containing application services under the `apps/` directory.

Agents should follow these conventions when reading, modifying, or extending the code.

---

# Repository Overview

Root project name: `eduweaver`

Primary application currently present:

```
apps/
  ingestion_service/
    app/
      main.py
      adapters/
      indexing/
      pipeline/
```

The ingestion service processes documents through a pipeline:

parse → normalize → chunk → embed → index

Key modules:

- `pipeline/` – document processing stages
- `indexing/` – vector indexing logic
- `adapters/` – integration points (external systems, APIs, etc.)
- `main.py` – entrypoint used for CLI execution

---

# Environment Setup

The project uses **uv** for dependency management and execution.

Python version:

```
>= 3.13
```

Install dependencies:

```
uv sync
```

Create virtual environment (if not already present):

```
uv venv
```

Run commands inside the environment using:

```
uv run <command>
```

---

# Running the Ingestion Service

Current CLI entrypoint:

```
apps/ingestion_service/app/main.py
```

Run the ingestion pipeline on a file:

```
uv run python -m apps.ingestion_service.app.main somefile.pdf
```

Alternatively run from the service directory:

```
cd apps/ingestion_service
uv run python -m app.main somefile.pdf
```

Agents should prefer **module execution (`-m`)** rather than running Python files directly.

---

# Build

The project currently has no compiled artifacts.

Build step is simply dependency resolution:

```
uv sync
```

If packaging becomes necessary later, build using:

```
uv build
```

---

# Linting

The repository includes a `.ruff_cache`, indicating that **Ruff** is used for linting.

Run lint:

```
uv run ruff check .
```

Auto-fix lint issues:

```
uv run ruff check . --fix
```

Format code:

```
uv run ruff format .
```

Agents should run Ruff formatting before committing code changes.

---

# Testing

There are currently **no test files in the repository**, but agents should assume
that `pytest` will be used when tests are introduced.

Expected test layout:

```
tests/
  test_pipeline.py
```

Run all tests:

```
uv run pytest
```

Run a specific test file:

```
uv run pytest tests/test_pipeline.py
```

Run a single test function:

```
uv run pytest tests/test_pipeline.py::test_chunk_document
```

Run tests matching a pattern:

```
uv run pytest -k chunk
```

Agents adding features should also add tests.

---

# Code Style Guidelines

## General Principles

- Prefer clarity over cleverness
- Keep functions small and focused
- Favor composition over inheritance
- Avoid hidden side effects

Pipeline stages should behave like **pure transformations when possible**.

---

# Imports

Use **absolute imports from the repository root**.

Example:

```
from apps.ingestion_service.app.pipeline.parse_document import parse_document
```

Avoid relative imports like:

```
from ..pipeline import parse_document
```

Import ordering:

1. Standard library
2. Third‑party libraries
3. Local project modules

Example:

```
import pathlib

import numpy as np

from apps.ingestion_service.app.pipeline.chunk_document import chunk_document
```

---

# Formatting

Formatting is enforced using **Ruff**.

General rules:

- 4 space indentation
- 88–100 column width
- trailing commas in multiline structures
- double quotes for strings

Example:

```
chunks = chunk_document(
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

Prefer built-in generics (Python 3.9+):

```
list[str]
dict[str, Any]
```

Avoid using `Any` unless absolutely necessary.

---

# Naming Conventions

Variables:

```
snake_case
```

Functions:

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

File names:

```
snake_case.py
```

---

# Error Handling

Do not swallow exceptions silently.

Bad:

```
try:
    process()
except Exception:
    pass
```

Good:

```
try:
    process()
except Exception as exc:
    raise RuntimeError("Document processing failed") from exc
```

Pipeline stages should raise **explicit, meaningful errors**.

---

# Logging

Prefer structured logging over print statements.

Example:

```
import logging

logger = logging.getLogger(__name__)
logger.info("Chunking document", extra={"chunks": len(chunks)})
```

Avoid `print()` except for CLI user feedback.

---

# Pipeline Design Guidelines

Pipeline modules should follow this pattern:

```
input -> transform -> output
```

Example structure:

```
parse_document()
normalize_document()
chunk_document()
generate_embeddings()
```

Each stage should:

- accept clear inputs
- return explicit outputs
- avoid global state

---

# When Modifying the Codebase

Agents should:

1. Keep functions small and composable
2. Avoid introducing circular imports
3. Maintain clear pipeline flow
4. Preserve deterministic behavior

When adding new pipeline steps:

- place them under `pipeline/`
- add clear docstrings
- add tests

---

# Files That Should Not Be Modified

Agents should **not modify**:

- `.venv/`
- `.ruff_cache/`
- `.git/`

These are environment or tooling artifacts.

---

# Future Improvements (Agents May Implement)

Recommended improvements:

- Add a `tests/` directory
- Introduce a proper CLI entrypoint
- Add structured logging configuration
- Introduce type checking with `mypy`
- Add CI lint + test workflow

Agents implementing these improvements should update this document accordingly.
