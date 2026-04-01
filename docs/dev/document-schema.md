# Document Schema

This document defines the **Normalized Document Schema** used across the system to represent technical content after ingestion.

The schema is designed to support multiple document types, including:

- scientific papers
- books
- technical documentation
- repositories
- code files
- markdown documents with images
- PDFs

The schema intentionally **does not depend on the original document format**. All sources are converted to the same internal representation.

The model is divided into three conceptual layers:

1. Document
2. Structure
3. Content Blocks

This design is conceptually similar to how **DOM trees or ASTs** represent structured information.

---

# 1. Document Layer

Represents the document as a whole.

Example fields:

```
document_id
title
source_type (pdf | markdown | repo | webpage | docx)
source_path
author
created_at
language
page_count
```

Additional metadata:

```
keywords
abstract
summary
```

Asset locations:

```
images_path
figures_path
```

This allows the system to support:

- PDFs
- books
- repositories
- technical documentation

---

# 2. Structure Layer

Represents the logical structure of the document.

Most technical documents contain a hierarchical structure:

- chapters
- sections
- subsections

Example schema:

```
Section
  section_id
  document_id
  title
  level
  order
  parent_section_id
  page_start
  page_end
```

Example hierarchy:

```
1 Introduction
1.1 Background
1.2 Related Work
2 Methodology
```

Section awareness is useful for retrieval because queries can prioritize the **relevant part of the document**.

---

# 3. Content Block Layer

This is the **core representation of document knowledge**.

Each piece of content is represented as a `ContentBlock`.

Example structure:

```
ContentBlock
  block_id
  document_id
  section_id
  page_number
  block_type
  order
  content
  metadata
```

Supported block types:

- paragraph
- equation
- figure
- table
- code
- list
- heading

---

# 4. Paragraph Blocks

```
type: paragraph
content: text
```

Metadata may include:

```
token_count
embedding
```

Paragraph blocks form the majority of document content.

---

# 5. Equation Blocks

Equations are stored explicitly so the tutor can explain them.

```
type: equation
content: LaTeX
```

Metadata:

```
latex
verbalization
variables_detected
```

Example equation:

```
R = K (W/db)^as N^e
```

Detected symbols:

```
R
W
db
N
```

This structure allows the tutor to explain variables and relationships.

---

# 6. Figure Blocks

Figures represent images, graphs, and diagrams extracted from the document.

```
type: figure
content: caption
```

Metadata:

```
image_url
image_description
figure_number
```

Example:

```
image_url: blob://documents/{id}/images/fig1.png
```

---

# 7. Table Blocks

Tables are represented with structured metadata.

```
type: table
```

Metadata:

```
table_data
columns
rows
```

---

# 8. Code Blocks

Code blocks allow the tutor to explain programming examples.

```
type: code
```

Metadata:

```
language
code
dependencies
```

---

# 9. Image Handling

Images extracted during parsing are stored separately in Blob Storage.

Example fields:

```
image_url
image_description
section_id
page
```

Example location:

```
blob://documents/{document_id}/images/fig1.png
```

---

# 10. Document Pre‑Digest

During ingestion the system generates a **document pre‑digest** that summarizes the document.

Generated metadata includes:

```
document_summary
key_concepts
topic_tags
section_summaries
```

Example summary:

```
"This paper studies prediction of drilling rate using artificial neural networks."
```

Example concepts:

```
rate of penetration
drilling optimization
neural networks
weight on bit
```

This metadata helps the tutor understand the **overall topic of the document**.

---

# 11. Chunking Strategy

Chunking converts content blocks into retrieval units for RAG.

Rules:

1. Preserve document structure
2. Merge small paragraphs
3. Maintain chunk size between **200–400 tokens**
4. Keep equations with their explanatory text

Example semantic chunk:

```
Paragraph
Equation
Paragraph
```

These may be merged into a single chunk to preserve context.

---

# 12. Retrieval Notes

Retrieval operates primarily using:

- hybrid search (vector + keyword)
- document‑scoped filtering

```
filter: document_id
```

Future versions may include **agentic retrieval strategies**, but the MVP uses deterministic retrieval.

---

# 13. Summary

The document schema provides a unified representation of technical documents.

Key design principles:

- format‑agnostic representation
- structure awareness
- explicit representation of equations, figures, and code
- compatibility with RAG retrieval

This schema acts as the **foundation for the ingestion pipeline and tutor reasoning system**.
