# MVP Milestone 03 — Tutor Service (RAG Integration)

This milestone implements the **AI Tutor Service** that combines document retrieval with a Large Language Model (LLM) to generate contextual explanations for users.

It builds directly on:

- **Milestone 01 — Document Ingestion** (documents parsed and indexed)
- **Milestone 02 — Retrieval Layer** (relevant chunks can be retrieved)

The goal of this milestone is to validate the **core RAG loop**:

```
User Question
  ↓
Retrieval
  ↓
Prompt Assembly
  ↓
LLM
  ↓
Answer grounded in document context
```

This is the first milestone where the system behaves like a **functional AI tutor**, although still without a full application API or frontend.

---

# 1. Milestone Goal

Create a working Tutor Service capable of answering questions about a document using Retrieval-Augmented Generation (RAG).

Expected pipeline:

```
User Question
  ↓
Retrieval Layer
  ↓
Context Assembly
  ↓
Prompt Construction
  ↓
LLM Provider
  ↓
Tutor Response
```

The system must generate **clear explanations grounded in retrieved document context**.

---

# 2. Scope

Included in this milestone:

- Tutor Service implementation
- RAG pipeline integration
- prompt assembly
- LLM provider integration
- citation support
- explanation formatting

Excluded from this milestone:

- frontend UI
- application API
- authentication
- document library

---

# 3. Components Involved

Services used in this milestone:

- tutor-service
- vector database
- LLM provider

Relevant documentation:

- docs/dev/tutor-prompt-architecture.md
- docs/dev/retrieval-architecture.md
- docs/dev/system-architecture.md

---

# 4. Implementation Tasks

## Task 1 — Tutor Service Skeleton

Create the base tutor service.

Suggested location:

```
apps/tutor-service/
```

Basic structure:

```
app/
  main.py
  retrieval/
  prompts/
  providers/
  tools/
```

The service should expose a simple endpoint or function for querying the tutor.

Example interface:

```
ask_tutor(question, document_id)
```

---

## Task 2 — Retrieval Integration

Connect the retrieval module from **Milestone 02**.

Pipeline:

```
question
  ↓
retrieve_chunks()
  ↓
top_k_chunks
```

Expected output:

- paragraph chunks
- equation chunks
- supporting context

---

## Task 3 — Context Assembly

Combine retrieved chunks into a structured context block.

Example structure:

```
Document Summary
Key Concepts

Retrieved Context
-----------------
Chunk 1
Chunk 2
Chunk 3
```

This context will be passed to the LLM.

---

## Task 4 — Prompt Construction

Implement prompt assembly based on:

```
docs/dev/tutor-prompt-architecture.md
```

Prompt layers:

```
System Instructions
Document Summary
Key Concepts
Retrieved Context
User Question
```

Example instruction:

```
You are an AI tutor helping a student understand a technical document.
Explain concepts clearly and reference the document context.
```

---

## Task 5 — LLM Provider Integration

Integrate a language model provider.

Possible providers:

- Azure OpenAI
- OpenAI
- local models (Ollama)

The provider should be abstracted behind a small interface:

```
generate_response(prompt)
```

---

## Task 6 — Citation Support

Responses should include references to the source chunks.

Example response format:

```
Answer:
The equation describes the relationship between drilling parameters...

Sources:
- Section: ROP Models
- Page: 5
```

This helps users verify explanations.

---

## Task 7 — Tutor Test Script

Create a simple script that tests the tutor service without the frontend.

Example queries:

```
Explain the ROP equation
What variables influence drilling rate?
What does WOB mean?
```

Expected output:

- explanation
- citations
- grounded answers

---

# 5. Acceptance Criteria

This milestone is complete when:

- tutor responses use retrieved document context
- explanations are coherent and structured
- responses include source references
- equation explanations work for common cases

---

# 6. Deliverables

Working components:

- tutor-service
- prompt assembly module
- LLM provider integration
- tutor test scripts

---

# 7. Success Metric

The milestone is successful if:

- the tutor answers questions using document context
- equations are explained clearly
- responses include citations
- response latency remains under ~5 seconds

Once this milestone is validated, the next milestone is:

**MVP Milestone 04 — Application API**
