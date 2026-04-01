# Retrieval Architecture

This document defines the **retrieval system** used by the AI tutor to locate relevant knowledge from ingested documents.

The goal of retrieval is to supply the language model with **high‑quality, contextually relevant information** before generating a response.

In Retrieval-Augmented Generation (RAG) systems, retrieval quality has a larger impact on answer quality than the model itself.

---

# 1. Design Goals

The retrieval system must:

- Provide **accurate document context** for questions
- Work across **multiple documents in a user library**
- Prioritize **relevant sections of the current document**
- Support **technical content types** (equations, figures, code)
- Avoid cross‑document contamination
- Maintain low latency for interactive tutoring

---

# 2. Retrieval Scope

Retrieval is always **document-scoped by default**.

When a user opens a document, all searches must be filtered by the active document.

```
filter: document_id = current_document
```

This prevents unrelated context from other documents in the user's library.

Future versions may support:

- cross‑document research
- multi-document comparison
- knowledge graph traversal

---

# 3. Retrieval Pipeline

The retrieval pipeline follows this process:

```
User Question
     ↓
Query Processing
     ↓
Search Strategy
     ↓
Vector Search
     ↓
Keyword Search
     ↓
Result Ranking
     ↓
Context Assembly
     ↓
LLM Prompt
```

This layered approach improves recall and precision.

---

# 4. Query Processing

Before searching the index, the query may be enriched with additional context.

Possible inputs:

- user question
- selected text (optional)
- document summary
- section context

Example:

User question:

"Explain the equation above"

If text was selected in the reader, the system attaches:

```
selected_text
page_number
section_title
```

This significantly improves retrieval precision.

---

# 5. Hybrid Search

The retrieval system uses **hybrid search**, combining:

- vector search
- keyword search

Vector search captures semantic similarity.

Keyword search captures exact technical matches.

Example:

Vector search retrieves conceptually related paragraphs.

Keyword search retrieves exact terms such as:

- variable names
- formulas
- technical identifiers

Results from both methods are merged and ranked.

---

# 6. Vector Search

Vector search retrieves semantically similar chunks.

Example embedding query:

```
Explain the drilling rate equation
```

The embedding model retrieves chunks discussing:

- drilling parameters
- rate of penetration
- mathematical models

Each chunk includes metadata:

```
document_id
section_title
block_type
page_number
```

---

# 7. Keyword Search

Keyword search is especially useful for technical documents.

Examples where keyword search is valuable:

- equation symbols
- variable names
- programming functions
- technical terminology

Example:

```
WOB
ROP
gradient descent
neural network
```

Keyword search ensures exact matches are not missed.

---

# 8. Chunk Ranking

Retrieved chunks are ranked before being sent to the LLM.

Ranking signals may include:

- semantic similarity score
- keyword match score
- section relevance
- chunk type priority

Example priorities:

| Chunk Type | Priority |
|------------|----------|
| equation | high |
| paragraph | medium |
| figure | medium |
| code | high |
| table | medium |

Equations and code blocks often receive higher priority because they represent key technical information.

---

# 9. Context Window Assembly

The top ranked chunks are assembled into the final context provided to the LLM.

Typical limits:

- 3–8 chunks
- 800–2000 tokens

Chunks are ordered to preserve logical flow:

```
Section context
Paragraph explanation
Equation
Supporting paragraph
```

Maintaining order helps the model understand the reasoning chain.

---

# 10. Section-Aware Retrieval

The system prioritizes chunks from the **same section** when possible.

Example:

If the question refers to an equation in section "ROP Models", retrieval should prioritize:

- chunks from "ROP Models"
- chunks from nearby sections

This improves contextual consistency.

---

# 11. Selection-Based Retrieval

If the user selects text inside the reader, the system may use the selected snippet as a retrieval query.

Example workflow:

```
User selects equation
↓
"Ask Tutor"
↓
Selected text becomes retrieval query
```

This method often produces more accurate results than natural language questions alone.

---

# 12. Agentic Retrieval (Future Phase)

Future versions may implement **agentic retrieval**.

In this approach, the agent decides which retrieval strategy to use.

Possible tools:

- retrieve_equation_context
- retrieve_section_context
- retrieve_code_context
- web_search

The agent may execute multiple retrieval steps before answering.

For the MVP, retrieval remains deterministic.

---

# 13. Fallback Strategies

If document retrieval fails to produce sufficient context, the system may:

1. Expand the search to the full document
2. Search related sections
3. Perform external web search

External search must be clearly labeled as supplemental information.

---

# 14. Retrieval Providers

Supported backends:

- Azure AI Search
- Qdrant

Both support:

- vector search
- metadata filters
- hybrid search

The retrieval layer should remain **provider‑agnostic**.

---

# 15. Performance Considerations

Retrieval must remain fast enough for interactive reading.

Target latency:

- Retrieval: <300 ms
- Full response: <5 seconds

Techniques to improve performance:

- caching
- query rewriting
- precomputed embeddings

---

# 16. Summary

The retrieval architecture relies on four key principles:

1. **Document-scoped search**
2. **Hybrid retrieval (vector + keyword)**
3. **Structure-aware ranking**
4. **Context assembly for LLM reasoning**

This system allows the tutor to retrieve precise technical knowledge from complex documents.
