# AI Search - Chunking

Este es el enfoque recomendado cuando tu PDF tiene **gráficas, fórmulas matemáticas, tablas complejas o diagramas**. Usamos el **Document Layout Skill** (el más potente de Azure AI Search en 2026) que:

- Extrae el documento con el modelo Layout de Document Intelligence.
- Hace **chunking inteligente** directamente en el skill (¡con control total de tamaño y overlap!).
- Extrae imágenes/gráficos con su posición exacta en la página (locationMetadata).
- Convierte tablas en Markdown legible y detecta estructura de fórmulas.

### Ventajas y desventajas del flujo manual (vs automático AzureBlobKnowledgeSource)

| Aspecto                          | Flujo MANUAL (este tutorial)                                                 | Flujo AUTOMÁTICO (AzureBlobKnowledgeSource)     |
| -------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------- |
| **Control de chunking**          | Total (máx. longitud + overlap + respeta párrafos/tablas)                    | Muy limitado (solo 2 modos: MINIMAL o STANDARD) |
| **Tablas / Fórmulas / Gráficos** | Excelente (tablas en Markdown, imágenes con posición, estructura preservada) | Bueno pero black-box, sin metadata de posición  |
| **Personalización**              | Ilimitada (añadir skills, campos extra, verbalización de imágenes)           | Casi nula (no puedes tocar skillset)            |
| **Complejidad**                  | Alta (5-6 recursos a crear)                                                  | Baja (solo 1 Knowledge Source)                  |
| **Tiempo de setup**              | 15-30 min + reindexación                                                     | 2 minutos                                       |
| **Costo durante ingestión**      | Más alto (Document Intelligence + embeddings)                                | Menor                                           |
| **Mejor para**                   | PDFs técnicos, científicos, con ecuaciones, diagramas                        | Prototipos rápidos o PDFs simples               |

**Recomendación**: Usa este flujo manual si tus PDFs son complejos. Si solo quieres velocidad, quédate con el automático.

### Tutorial completo – Código Python

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import *
from azure.search.documents.indexes.models import (
    DocumentIntelligenceLayoutSkill,
    TextSplitSkill, AzureOpenAIEmbeddingSkill,
    SearchIndexerDataSourceConnection, SearchIndex, SearchIndexer,
    SearchIndexKnowledgeSource, SearchIndexKnowledgeSourceParameters,
    SearchIndexFieldReference, KnowledgeBase, KnowledgeBaseAzureOpenAIModel,
    KnowledgeSourceReference, KnowledgeRetrievalOutputMode
)

# ==================== CONFIGURACIÓN ====================
search_endpoint = "https://<tu-search>.search.windows.net"
search_key = "<tu-key>"
blob_connection = "DefaultEndpointsProtocol=https;AccountName=..."
container_name = "mi-contenedor-pdfs"
aoai_endpoint = "https://<tu-aoai>.openai.azure.com/"
aoai_key = "<tu-aoai-key>"
aoai_embedding = "text-embedding-3-large"
aoai_chat = "gpt-5-mini"
doc_intel_endpoint = "https://<tu-doc-intel>.cognitiveservices.azure.com/"  # o usa Foundry

client = SearchIndexClient(search_endpoint, AzureKeyCredential(search_key))
indexer_client = SearchIndexerClient(search_endpoint, AzureKeyCredential(search_key))

# 1. DATA SOURCE (Blob)
datasource = SearchIndexerDataSourceConnection(
    name="mi-pdf-ds",
    type="azureblob",
    connection_string=blob_connection,
    container=SearchIndexerDataContainer(name=container_name)
)
client.create_or_update_data_source_connection(datasource)

# 2. SKILLSET con Document Intelligence + chunking controlado
skills = [
    # === Document Layout Skill (el corazón) ===
    DocumentIntelligenceLayoutSkill(
        name="layout-skill",
        description="Extrae texto, tablas y gráficos con chunking controlado",
        context="/document",
        output_mode="oneToMany",
        output_format="text",                    # "markdown" también funciona
        extraction_options=["images", "locationMetadata"],
        chunking_properties={
            "unit": "characters",
            "maximum_length": 2000,              # ← TU CONTROL AQUÍ
            "overlap_length": 200                # ← Y AQUÍ (ideal para contexto)
        },
        inputs=[InputFieldMapping(name="file_data", source="/document/file_data")],
        outputs=[
            OutputFieldMapping(name="text_sections", target_name="text_sections"),
            OutputFieldMapping(name="normalized_images", target_name="normalized_images")
        ]
    ),
    # === Embedding de los chunks ===
    AzureOpenAIEmbeddingSkill(
        name="embedding-skill",
        context="/document/text_sections/*",
        resource_url=aoai_endpoint,
        api_key=aoai_key,
        deployment_name=aoai_embedding,
        inputs=[InputFieldMapping(name="text", source="/document/text_sections/*/content")],
        outputs=[OutputFieldMapping(name="vector", target_name="content_embedding")]
    )
]

skillset = SearchIndexerSkillset(
    name="mi-pdf-skillset",
    description="Document Intelligence + chunking para PDFs complejos",
    skills=skills,
    cognitive_services=SearchIndexerAIServicesByIdentity(subdomain_url=doc_intel_endpoint)
)
client.create_or_update_skillset(skillset)

# 3. ÍNDICE (campos optimizados para Agentic RAG)
fields = [
    SimpleField(name="id", type="Edm.String", key=True),
    SearchableField(name="content", type="Edm.String", searchable=True),
    SearchField(name="content_embedding", type="Collection(Edm.Single)", 
                vector_search_dimensions=3072, vector_search_profile_name="hnsw"),
    SimpleField(name="page_number", type="Edm.Int32", filterable=True),
    ComplexField(name="location_metadata", fields=[
        SimpleField(name="pageNumber", type="Edm.Int32"),
        SimpleField(name="boundingPolygon", type="Edm.String")
    ]),
    SearchableField(name="document_title", type="Edm.String")
]

vector_search = VectorSearch(
    profiles=[VectorSearchProfile(name="hnsw", algorithm_configuration_name="hnsw-config")],
    algorithms=[HnswAlgorithmConfiguration(name="hnsw-config")]
)

index = SearchIndex(name="mi-pdf-index-complejo", fields=fields, vector_search=vector_search)
client.create_or_update_index(index)

# 4. INDEXER (ejecuta todo)
indexer = SearchIndexer(
    name="mi-pdf-indexer",
    data_source_name="mi-pdf-ds",
    target_index_name="mi-pdf-index-complejo",
    skillset_name="mi-pdf-skillset",
    field_mappings=[FieldMapping(source_field_name="metadata_storage_name", target_field_name="document_title")]
)
indexer_client.create_or_update_indexer(indexer)

print("🚀 Ejecuta el indexer: indexer_client.run_indexer('mi-pdf-indexer')")
```

### 5. Knowledge Source + Knowledge Base (Agentic RAG)

```python
# Knowledge Source (apunta al índice que creamos)
ks = SearchIndexKnowledgeSource(
    name="mi-pdf-ks",
    description="Índice manual con Document Intelligence",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name="mi-pdf-index-complejo",
        source_data_fields=[
            SearchIndexFieldReference(name="content"),
            SearchIndexFieldReference(name="page_number"),
            SearchIndexFieldReference(name="document_title")
        ]
    )
)
client.create_or_update_knowledge_source(ks)

# Knowledge Base (el agente)
kb = KnowledgeBase(
    name="mi-pdf-kb",
    knowledge_sources=[KnowledgeSourceReference(name="mi-pdf-ks")],
    models=[KnowledgeBaseAzureOpenAIModel(
        azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
            resource_url=aoai_endpoint, deployment_name=aoai_chat
        )
    )],
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort,
    answer_instructions="Responde en español, cita página y describe tablas/gráficos si aparecen."
)
client.create_or_update_knowledge_base(kb)
```

### 6. Consultar

Usa exactamente el mismo `KnowledgeBaseRetrievalClient` de la página que te pasé originalmente, pero cambiando el nombre de la Knowledge Base a `"mi-pdf-kb"`.

### Consejos extra para PDFs con fórmulas/gráficos

- Cambia `maximum_length` a 800-1500 según tu caso (más pequeño = más preciso).
- Si quieres verbalizar gráficos: añade un skill `AzureOpenAIChatCompletionSkill` para describir imágenes.
- Tablas aparecen como Markdown en el campo `content` → el agente las entiende perfectamente.
- Usa `location_metadata` para filtrar por página en consultas avanzadas.
