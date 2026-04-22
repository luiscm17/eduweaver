# MVP Milestone 01 — Document Ingestion Prototype

This milestone implements the **first functional core of the system**: the document ingestion pipeline.

The objective is to validate that a technical document can be:

1. Uploaded
2. Parsed
3. Converted into structured blocks
4. Chunked
5. Embedded
6. Indexed in the vector database

No UI or tutor interaction is required in this milestone. The goal is purely to validate the **knowledge pipeline**.

---

# 1. Milestone Goal

Create a working ingestion pipeline capable of transforming a PDF into retrievable chunks.

Expected pipeline:

```
PDF
 ↓
Parser
 ↓
ContentBlocks
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Database
```

Once completed, the system must support **manual retrieval queries** against the indexed document.

---

# 2. Scope

Included in this milestone:

- PDF ingestion
- parsing using Docling (leveraging layout-aware Document trees and metadata) or Azure Document Intelligence
- normalization to Document Schema
- semantic chunking
- embedding generation
- vector indexing

Excluded from this milestone:

- frontend
- tutor service
- user authentication
- document library UI

---

# 3. Components Involved

Services used in this milestone:

- ingestion-service
- vector database
- blob storage (Azurite / Azure)

Relevant documentation:

- docs/dev/document-schema.md
- docs/dev/ingestion-pipeline.md
- docs/dev/retrieval-architecture.md

---

## Task 0 — Blob Storage Adapter & Config

Goal: design the configuration and adapter that allow the ingestion service to access PDFs stored in Azure Blob Storage or Azurite before parsing.

Steps:

- implement `app/config/settings.py` to load Azure credentials via environment variables
- expose helpers in `app/config/credentials.py` for SAS generation or token refresh as needed
- create `app/adapters/blob_storage.py` that lists blobs and yields read streams or SAS URLs
- ensure downstream parsers consume the provided stream instead of expecting a local download

This task centralizes secrets and keeps the pipeline agnostic of the storage provider.

---

# 4. Implementation Tasks

## Task 1 — File Upload Simulation

Goal: simulate the ingestion entry point.

Steps:

- place a test PDF in a local folder or Blob Storage
- create a script that triggers the ingestion pipeline

Example test file:

```
resources/test-document.pdf
```

---

## Task 2 — Parser Integration

Goal: extract structured data from the PDF.

Possible implementations:

- Docling parser (leveraging the Docling Document tree, furniture/groups, and layout metadata for enrichment)
- Azure Document Intelligence

Expected output:

- headings
- paragraphs
- equations
- figures
- tables

### Parser File Layout

Implement the Docling parser with the following modules inside `apps/ingestion_service/app/pipeline/docling/`:

- `engine.py`: orchestrates the Docling pipeline, downloads blobs, and configures `PdfPipelineOptions` (Granite/VLM) so you can request layout metadata.
- `parser.py`: walks the produced `DoclingDocument` (body/furniture/groups) and emits raw blocks with `type`, `content`, `page`, `bbox` and other metadata.
- `normalizer.py`: (optional for later) cleans edge cases, but for the milestone the parser should already provide normalized text.
- `section_builder.py`: groups consecutive blocks using Docling's hierarchy, assigning `section_id` and `level`.
- `chunker.py`: stub that will later consume `ContentBlock` entries and produce 200–400 token chunks.
- `run_local.py`: helper script that downloads the blob, runs the parser, and exports Markdown/JSON for inspection.

### Parser Responsibilities

- Use Docling's `DocumentStream` to feed the PDF (Blob download done in `engine.extract`).
- Preserve layout metadata (bounding boxes, fonts, page numbers) by copying `item.metadata` into the output before mapping to domain models.
- Map Docling `groups` → sections and `items` (code/formula/table) → typed blocks, storing `metadata` for later chunking.
- Emit outputs that can be directly fed into `app/domain/document.py`, `section.py`, and `content_block.py`.

### Starter snippet

```python
from apps.ingestion_service.app.pipeline.docling.engine import DoclingEngine
from apps.ingestion_service.app.pipeline.docling.parser import parse_docling_document

engine = DoclingEngine(vlm_endpoint=..., vlm_model=..., vlm_api_key=...)
doc, markdown = engine.extract('Artificial_Neural_Network_Model_for_Prediction_of_Drilling_Rate.pdf')
blocks = parse_docling_document(doc)
for block in blocks['items']:
    print(block['type'], block['metadata'].get('page'), block['content'][:60])
```

This snippet demonstrates the flow: `engine` downloads the blob and returns a Docling document, while `parser` turns it into layout-aware blocks ready to populate the domain models.

---

## Task 3 — Normalization

Goal: convert parsed data into the **Normalized Document Schema**. Docling already provides enriched blocks (with layout metadata, tables, formulas, groups, etc.), so the task is to map those nodes to Document/Section/ContentBlock while preserving the semantic structure exposed by Docling.

Output objects:

```
Document
Section
ContentBlock
```

Each block must include:

- block_type
- section_id
- content
- metadata

---

## Task 4 — Chunking

Goal: transform content blocks into semantic chunks suitable for RAG.

Rules:

- merge small paragraphs
- keep equations with explanation
- chunk size: 200–400 tokens

Output:

```
Chunk
  chunk_id
  document_id
  content
  metadata
```

---

## Task 5 — Embedding Generation

Goal: convert chunks into vector embeddings.

Possible models:

- Azure OpenAI embeddings
- OpenAI embeddings
- local embedding models

Each chunk must produce:

```
embedding_vector
```

---

## Task 6 — Vector Indexing

Goal: store embeddings in the vector database.

Possible databases:

- Azure AI Search
- Qdrant

Stored metadata must include:

- document_id
- section_title
- block_type
- page_number

---

## Task 7 — Retrieval Test

Goal: verify that relevant chunks can be retrieved.

Example test query:

```
"Explain the ROP equation"
```

Expected result:

- chunk containing the equation
- surrounding explanatory text

---

# 5. Acceptance Criteria

This milestone is considered complete when:

- A PDF can be ingested successfully
- ContentBlocks are generated
- Semantic chunks are created
- Embeddings are stored in the vector database
- Retrieval returns relevant chunks

---

# 6. Deliverables

Working components:

- ingestion-service prototype
- parsing integration
- chunking module
- embedding generation
- vector index integration

Artifacts produced:

- normalized_document.json
- chunks.json

---

# 7. Success Metric

The milestone is successful if:

- retrieval returns relevant technical context
- equations remain associated with their explanations
- chunks preserve document structure

Once this milestone works reliably, the next step is:

**MVP Milestone 02 — Retrieval + Tutor Integration**
