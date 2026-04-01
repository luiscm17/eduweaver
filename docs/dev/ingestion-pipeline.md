# Document Ingestion Pipeline

This document defines the **Universal Document Ingestion Pipeline** used by the system to process technical content such as PDFs, books, repositories, documentation, and web pages.

The goal of the pipeline is to convert heterogeneous sources into a **Normalized Document Format (NDF)** that can be indexed and used by the AI tutor.

---

# 1. Design Goals

The ingestion pipeline must:

- Support **multiple document sources**
- Extract **structured technical content**
- Preserve **document structure** (sections, equations, figures, code)
- Generate **semantic chunks for RAG**
- Produce **document metadata for tutor context**
- Store assets such as images and diagrams

The output of the pipeline must be independent from the original document format.

---

# 2. Supported Source Types

The system supports multiple document sources.

| Source Type | Examples |
|-------------|----------|
| PDF | scientific papers, books |
| DOCX | research drafts, documentation |
| Markdown | technical docs, README files |
| Repository | GitHub repositories |
| Web Page | technical blogs, documentation sites |

Each source is processed through a **Source Adapter** before normalization.

---

# 3. High Level Pipeline

The ingestion pipeline follows this sequence:

```
Document Upload
   ↓
Blob Storage
   ↓
Ingestion Trigger
   ↓
Source Adapter
   ↓
Parser
   ↓
Normalization
   ↓
Content Blocks
   ↓
Chunking
   ↓
Embeddings
   ↓
Indexing
```

The pipeline is executed asynchronously after the document is uploaded.

---

# 4. Storage Architecture

Documents and assets are stored in **Azure Blob Storage**.

Recommended structure:

```
documents/
  {document_id}/
      original/
          source.pdf
      images/
          figure1.png
          figure2.png
      assets/
          tables/
          diagrams/
      processed/
          normalized_document.json
          chunks.json
```

This structure allows:

- asset reuse
- debugging
- re-indexing without re-parsing

---

# 5. Source Adapters

Each document type uses an adapter that converts the source into an intermediate representation.

## PDF Adapter

Supported parsers:

- Azure Document Intelligence
- Docling

Extracted elements:

- headings
- paragraphs
- equations (LaTeX)
- figures
- tables

---

## Markdown Adapter

Parser extracts:

- headings
- paragraphs
- lists
- code blocks
- images
- links

Images referenced in markdown are downloaded and stored as assets.

---

## DOCX Adapter

Possible parsers:

- python-docx
- Azure Document Intelligence

Extracted elements:

- headings
- paragraphs
- tables
- images

---

## Repository Adapter

Repository ingestion includes:

- README files
- markdown documentation
- source code
- configuration files

The adapter may clone the repository and scan:

```
README.md
docs/
*.md
*.py
*.js
*.ts
```

---

## Web Adapter

Web pages are parsed using an HTML parser.

Extracted elements:

- headings
- paragraphs
- images
- code blocks
- links

The system removes navigation and irrelevant page elements.

---

# 6. Normalized Document Format (NDF)

All parsed documents are converted into a common structure.

```
Document
  Sections
  ContentBlocks
```

This ensures that downstream components do not depend on the original document format.

---

# 7. Content Blocks

The document is decomposed into **ContentBlocks**.

Possible block types:

- paragraph
- equation
- figure
- table
- code
- list
- heading

Example structure:

```
ContentBlock
  block_id
  document_id
  section_id
  block_type
  page_number
  content
  metadata
```

Examples:

Equation block:

```
block_type: equation
latex: R = K (W/db)^as N^e
```

Figure block:

```
block_type: figure
image_url: blob://documents/123/images/fig1.png
caption: Relation of ROP with N
```

Code block:

```
block_type: code
language: python
```

---

# 8. Chunking Strategy

Chunking must preserve document structure.

Rules:

1. Do not break equations from their explanation.
2. Merge small paragraphs.
3. Maintain chunk size between **200 and 400 tokens**.
4. Preserve section boundaries when possible.

Example:

```
Paragraph
Equation
Paragraph
```

These three blocks may form a single semantic chunk.

---

# 9. Embeddings

Each chunk is converted into a vector embedding.

Possible providers:

- Azure OpenAI embeddings
- OpenAI embeddings
- local embedding models

Stored metadata includes:

- document_id
- section_title
- block_type
- page_number

---

# 10. Indexing

Chunks are indexed in a vector database.

Possible backends:

Azure AI Search
Qdrant

Important rule:

Retrieval must be **document-scoped**.

```
filter: document_id = current_document
```

This prevents cross-document context contamination.

---

# 11. Document Pre-Digest

During ingestion the system generates a **document pre-digest**.

Generated metadata:

- document summary
- key concepts
- topic tags
- section summaries

Example:

```
summary: Prediction of drilling rate using neural networks

key concepts:
 - rate of penetration
 - drilling optimization
 - neural networks
```

This information is later used by the **Tutor Prompt Architecture**.

---

# 12. Trigger Architecture

The ingestion process is triggered automatically after upload.

Example architecture:

```
User Upload
   ↓
Backend API
   ↓
Azure Blob Storage
   ↓
Blob Event Trigger
   ↓
Azure Function
   ↓
Ingestion Pipeline
```

This allows asynchronous document processing.

---

# 13. Future Improvements

Possible enhancements include:

- incremental indexing
- distributed ingestion workers
- semantic chunk refinement
- concept graph extraction
- automatic prerequisite detection

These features can be added without changing the normalized document format.

---

# 14. Summary

The ingestion pipeline converts heterogeneous sources into structured knowledge.

Key ideas:

- universal document adapters
- normalized document format
- structure-aware chunking
- document-scoped retrieval

This pipeline forms the **foundation of the AI tutor knowledge system**.
