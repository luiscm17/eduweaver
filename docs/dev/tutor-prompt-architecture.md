# Tutor Prompt Architecture

This document defines how the AI tutor receives context and generates answers when a user interacts with a document (PDF, book, markdown, or code repository).

The goal is to transform a basic "chat with PDF" into a **context‑aware scientific tutor** capable of explaining technical material, equations, and code.

---

# 1. Design Goals

The tutor must:

- Understand the **topic of the document** before answering questions
- Use **retrieved context from the document**
- Explain **equations, figures, and code** clearly
- Avoid hallucinating information outside the document
- Provide **step‑by‑step explanations when appropriate**

To achieve this, the system provides structured context to the LLM before each response.

---

# 2. Prompt Context Layers

The tutor receives context in multiple layers. Each layer adds knowledge about the document.

Order matters.

```
System Instructions
Document Summary
Document Metadata
Retrieved Chunks
User Question
```

---

# 3. System Instructions

Defines the behavior of the tutor.

Example:

You are an AI tutor helping a student understand technical documents.

Rules:

- Prefer explanations grounded in the provided document context.
- If the question refers to an equation, explain the meaning of each variable.
- When useful, provide step‑by‑step explanations.
- If the document does not contain enough information, you may supplement with general scientific knowledge.
- If the question is unclear, ask for clarification.

Tone:

- Clear
- Educational
- Structured

---

# 4. Document Pre‑Digest Context

When a document is ingested, a **pre‑digest step** generates high‑level metadata.

This avoids forcing the model to read the entire document for every query.

Generated fields:

Document Summary

Short description of the document.

Example:

"This paper studies prediction of drilling rate using artificial neural networks and optimization of drilling parameters."

Key Concepts

List of main concepts extracted from the document.

Example:

- rate of penetration
- drilling optimization
- neural networks
- weight on bit

Section Titles

List of main sections of the document.

Example:

- Introduction
- ROP Models
- Artificial Neural Networks
- Results

This context helps the tutor understand **what the document is about** before answering.

---

# 5. Retrieval Context

When a user asks a question, the system retrieves relevant content blocks from the index.

Retrieval is always **document‑scoped**.

```
filter: document_id = current_document
```

The retrieved content may include:

- paragraphs
- equations
- figures
- tables
- code blocks

Each retrieved chunk includes metadata:

```
chunk_type
section_title
page_number
content
```

Example retrieval context:

Section: ROP Models

Equation:

R = K (W/db)^as N^e

Explanation:

R = rate of penetration
W = weight on bit
db = bit diameter
N = rotation speed

---

# 6. Prompt Assembly

The final prompt sent to the model is constructed as follows:

```
SYSTEM
Tutor instructions

DOCUMENT CONTEXT
Document summary
Key concepts
Section titles

RETRIEVED CONTEXT
Relevant chunks from the document

USER QUESTION
User message
```

Example structure:

```
You are an AI tutor helping explain a technical document.

Document summary:
This paper studies prediction of drilling rate using neural networks.

Key concepts:
- rate of penetration
- drilling optimization
- neural networks

Retrieved context:
[chunk 1]
[chunk 2]

User question:
Explain the equation shown above.
```

---

# 7. Equation Explanation Strategy

When the question references an equation, the tutor should:

1. Show the equation
2. Define each variable
3. Explain the relationship
4. Provide an example if possible

Example:

Equation:

R = K (W/db)^as N^e

Explanation structure:

Step 1 — Variables

R = rate of penetration
W = weight on bit
db = bit diameter
N = rotation speed

Step 2 — Interpretation

The equation models how drilling speed depends on mechanical parameters.

Step 3 — Example

Increasing rotation speed generally increases penetration rate until drilling conditions degrade.

---

# 8. Optional Tools

The tutor may call external tools when necessary.

Possible tools:

retrieve_document_context
retrieve_equation_context
web_search
generate_exercise

For the MVP, only **document retrieval** is required.

---

# 9. Future Improvements

Future versions of the tutor may include:

- prerequisite concept detection
- adaptive tutoring
- symbolic math validation
- code execution environments

These features will build on the same prompt architecture.

---

# 10. Summary

The tutor architecture is based on three core ideas:

1. **Document pre‑digest** gives the model high‑level understanding
2. **Structured retrieval** provides precise context
3. **Prompt layering** ensures reliable reasoning

This design allows the system to behave like a **context‑aware tutor rather than a simple chatbot**.
