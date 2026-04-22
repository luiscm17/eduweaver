# Azure AI Search Deep Dive for EduWeaver Ingestion Pipeline

This document analyzes how **Azure AI Search** can be integrated into the current EduWeaver ingestion architecture while preserving control of the pipeline defined in the MVP milestone.

Current architectural pipeline in the repository:

```
parse → normalize → chunk → embed → index
```

Directory structure already reflects this model:

```
pipeline/
  parse
  normalize
  chunk
  embed
indexing/
adapters/
```

The goal of this document is to understand **how Azure AI Search should be used without breaking this architecture**.

---

# 1. What Azure AI Search Actually Provides

Azure AI Search is not just a vector database. It provides four major subsystems:

1. **Indexes** – schema definition and storage
2. **Vector search** – approximate nearest neighbor search
3. **Semantic ranking** – transformer-based reranking
4. **Enrichment pipelines (Skillsets)** – automatic document processing

Architecture inside Azure Search:

```
Data Source
     ↓
Indexer
     ↓
Skillset (optional)
     ↓
Search Index
     ↓
Query Engine
```

However, EduWeaver **already owns its ingestion pipeline**, meaning:

```
Azure Indexers are optional
Azure Skillsets are optional
```

Azure Search becomes primarily:

```
Vector + hybrid retrieval engine
```

---

# 2. Why Not Use Azure Indexers

Azure Indexers are designed for ingestion from:

```
Azure Blob Storage
CosmosDB
SQL
SharePoint
```

Example indexer configuration:

```json
{
  "name": "docs-indexer",
  "dataSourceName": "blob-datasource",
  "targetIndexName": "documents",
  "schedule": { "interval": "PT2H" }
}
```

The problem for our pipeline:

- indexers assume **Azure manages ingestion**
- we lose control of parsing
- chunking becomes limited
- custom normalization is impossible

EduWeaver requires semantic chunking, equation preservation and structured blocks.

Therefore **indexers should not be used for the core pipeline**.

---

# 3. Document Intelligence Integration

Azure Document Intelligence extracts structure from PDFs:

```
paragraphs
tables
figures
equations
sections
```

Python example using the SDK:

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

client = DocumentIntelligenceClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)

poller = client.begin_analyze_document(
    "prebuilt-layout",
    document=file_bytes,
)

result = poller.result()

for paragraph in result.paragraphs:
    print(paragraph.content)
```

This produces a structured representation that fits perfectly with the **ContentBlock abstraction** defined in the milestone.

Example normalized block:

```python
ContentBlock(
    type="paragraph",
    text="Gradient descent updates parameters...",
    page=12,
)
```

Tables can be converted into structured blocks:

```python
ContentBlock(
    type="table",
    text="learning_rate | accuracy",
    page=14,
)
```

Keeping Document Intelligence **outside Azure Search skillsets** allows:

- full control of normalization
- semantic chunking
- better academic document support

---

# 4. Semantic Chunking vs Azure Split Skill

Azure provides a "Text Split Skill".

Example configuration:

```json
{
  "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
  "textSplitMode": "pages",
  "maximumPageLength": 1000
}
```

Problems:

- character-based chunking
- no semantic awareness
- breaks equations
- breaks sections

EduWeaver requires chunk logic like:

```
paragraph + explanation
equation + context
table + caption
```

Example custom chunker:

```python
def chunk_blocks(blocks: list[ContentBlock]) -> list[str]:
    chunks = []
    current = []

    for block in blocks:
        current.append(block.text)

        if token_length(current) > 350:
            chunks.append("\n".join(current))
            current = []

    if current:
        chunks.append("\n".join(current))

    return chunks
```

This level of control is **not possible inside Azure skillsets**.

---

# 5. Azure AI Search Vector Index Design

Vector fields are defined in the index schema.

Example minimal index:

```python
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
)
```

Recommended schema for EduWeaver:

```python
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        vector_search_dimensions=3072,
        vector_search_configuration="vector-config",
    ),
    SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
    SimpleField(name="page", type=SearchFieldDataType.Int32, filterable=True),
    SimpleField(name="block_type", type=SearchFieldDataType.String, filterable=True),
]
```

This supports:

- vector retrieval
- metadata filtering
- structured citations

---

# 6. Hybrid Retrieval

Azure Search supports **hybrid search** combining vector + keyword search.

Example query:

```python
results = search_client.search(
    search_text="gradient descent",
    vector={
        "value": embedding,
        "fields": "content_vector",
        "k": 5,
    },
)
```

Hybrid retrieval improves recall because:

- vector search captures semantics
- keyword search captures exact matches

Academic material benefits heavily from hybrid retrieval.

---

# 7. Semantic Ranking

Azure provides a transformer reranker.

Configuration example:

```python
results = search_client.search(
    search_text=query,
    semantic_configuration_name="semantic-config",
    query_type="semantic",
)
```

This stage reranks retrieved documents using a deep model.

Pipeline becomes:

```
vector retrieval
     ↓
keyword retrieval
     ↓
semantic reranking
```

This significantly improves RAG grounding.

---

# 8. Multimodal RAG

Azure supports indexing of:

```
text
images
tables
audio
video transcripts
```

Example multimodal block representation:

```python
ContentBlock(
    type="figure",
    text="Diagram of transformer architecture",
    image_path="figures/transformer.png",
)
```

Embeddings can be generated separately:

```
text embeddings
image embeddings
```

This enables queries like:

"show me the diagram explaining attention"

However multimodal RAG increases:

- infrastructure complexity
- storage
- embedding cost

Recommendation: **defer until phase 2**.

---

# 9. Agentic Retrieval

Azure introduced "Agentic Retrieval" integrating:

```
Azure AI Search
Azure OpenAI
tool use
function calling
```

However EduWeaver already implements:

```
Tutor Agent
↓
MCP tools
↓
retrieval
```

Conceptually this is already **agentic RAG**.

Azure's solution would duplicate existing capabilities.

---

# 10. Recommended Architecture

Final architecture for the system:

```
Blob Storage
      ↓
Ingestion Service
      ↓
Document Intelligence
      ↓
Normalization
      ↓
Semantic Chunking
      ↓
Embeddings (Azure OpenAI)
      ↓
Azure AI Search
```

Azure Search responsibilities:

```
vector search
hybrid search
semantic ranking
metadata filtering
```

Ingestion Service responsibilities:

```
parsing
document structure
semantic chunking
embedding generation
index uploads
```

---

# 11. Suggested Adapter Layer

To properly control Azure Search, the repository should introduce:

```
app/adapters/azure_search/
```

Suggested modules:

```
index_schema.py
index_manager.py
search_client.py
upload_client.py
```

Example index creation helper:

```python
def create_index(client, index_name, fields):
    index = SearchIndex(name=index_name, fields=fields)
    client.create_or_update_index(index)
```

Example document upload:

```python
search_client.upload_documents([
    {
        "id": "chunk-001",
        "content": text,
        "content_vector": embedding,
        "page": page,
    }
])
```

---

# 12. Key Architectural Principle

The ingestion service must remain the **source of truth for document transformation**.

Azure AI Search should be treated as:

```
retrieval infrastructure
```

not as:

```
document processing pipeline
```

Maintaining this boundary ensures the system remains extensible and predictable.

---

# Future Exploration Topics

Potential future investigations:

1. multimodal embeddings for diagrams
2. citation-aware chunk retrieval
3. hierarchical retrieval (section → chunk)
4. dynamic re-ranking with LLMs
5. learning-to-rank models for educational QA
