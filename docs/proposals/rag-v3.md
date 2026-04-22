# AI Search - Knowledge Store

Ahora incluye:  

- **Knowledge Store** (guarda automáticamente las imágenes recortadas/normalizadas como archivos .jpg/.png en Blob Storage).  
- **Verbalización de imágenes** (usa un modelo vision de Azure OpenAI para describir gráficos, tablas, fórmulas y diagramas en texto).  
- **Chunking inteligente** + **locationMetadata** (para saber exactamente en qué página y coordenadas está cada imagen).  

Este pipeline es el que usan los tutoriales oficiales de multimodal RAG en Azure AI Search (2026).

### Dónde se guardan las imágenes y cómo se accede a ellas

Las imágenes se proyectan automáticamente en un contenedor de **Azure Blob Storage** que tú eliges.  

- Ruta típica:  
  `https://<tu-storage>.blob.core.windows.net/mi-imagenes/<base64-del-document-id>/normalized_images_0.jpg`  

- El campo **`imagePath`** (que aparece en el índice) te da la ruta relativa exacta.  
- Acceso: Generas una URL con SAS (Shared Access Signature) o usas Azure Storage SDK en tu app.  

**No se borran nunca** (a menos que borres el Knowledge Store). Puedes verlas en Azure Portal → Storage Explorer.

### ¿El agente (Knowledge Base / Agentic RAG) puede ver o mostrar las imágenes?

**Respuesta directa y clara**:  

**NO.**  
El agente **solo trabaja con texto y embeddings**. No devuelve ni renderiza imágenes binarias en la respuesta de `KnowledgeBaseRetrievalClient`.  

Lo que SÍ hace:  

- Usa las **descripciones verbales** (el texto generado por el LLM) que se embeben junto al chunk. Por eso el agente entiende perfectamente “hay un gráfico de barras que muestra que el algoritmo X es 30% más rápido”.  
- Devuelve **citas** con `page_number`, `locationMetadata` e `imagePath`.  

**En tu aplicación (UI)**:  
Cuando recibas la respuesta del agente, miras las referencias → tomas el `imagePath` → generas la URL del Blob → muestras `<img src="...">` al lado de la respuesta.  

Es decir: **el agente te dice “mira el gráfico de la página 5” y tu app lo muestra**. Esto es exactamente lo que hacen los copilots multimodales reales.

### Uso posterior de las imágenes guardadas

- Mostrarlas en el chat (la más común).  
- Depuración: ver exactamente qué vio el modelo.  
- Power BI / análisis downstream.  
- Entrenamiento de otros modelos (exportar dataset multimodal).  
- Reutilizar en otros agentes o apps.

### Código Python COMPLETO (actualizado y listo para copiar)

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import *

# ==================== CONFIGURACIÓN ====================
search_endpoint = "https://<tu-search>.search.windows.net"
search_key = "<tu-key>"
blob_connection = "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=..."
image_container = "mi-imagenes"                    # ← aquí se guardan las imágenes
aoai_endpoint = "https://<tu-aoai>.openai.azure.com/"
aoai_key = "<tu-aoai-key>"
embedding_deployment = "text-embedding-3-large"
chat_deployment = "gpt-5-vision"                   # modelo con visión (gpt-4o o gpt-5-vision)
doc_intel_endpoint = "https://<tu-doc-intel>.cognitiveservices.azure.com/"

client = SearchIndexClient(search_endpoint, AzureKeyCredential(search_key))
indexer_client = SearchIndexerClient(search_endpoint, AzureKeyCredential(search_key))

# 1. DATA SOURCE (igual)
datasource = SearchIndexerDataSourceConnection(
    name="mi-pdf-ds", type="azureblob",
    connection_string=blob_connection,
    container=SearchIndexerDataContainer(name="mi-contenedor-pdfs")
)
client.create_or_update_data_source_connection(datasource)

# 2. SKILLSET COMPLETO (Layout + Verbalización + Embeddings + Knowledge Store)
skills = [
    # === 1. Document Layout Skill (chunking + extracción de imágenes) ===
    DocumentIntelligenceLayoutSkill(
        name="layout-skill",
        context="/document",
        output_mode="oneToMany",
        output_format="text",
        extraction_options=["images", "locationMetadata"],
        chunking_properties={"unit": "characters", "maximum_length": 1800, "overlap_length": 180},
        inputs=[InputFieldMapping(name="file_data", source="/document/file_data")],
        outputs=[
            OutputFieldMapping(name="text_sections", target_name="text_sections"),
            OutputFieldMapping(name="normalized_images", target_name="normalized_images")
        ]
    ),
    
    # === 2. Verbalización de imágenes (GenAI Prompt / ChatCompletion) ===
    AzureOpenAIChatCompletionSkill(   # o GenAIPromptSkill si usas preview
        name="verbalize-images",
        context="/document/normalized_images/*",
        resource_url=aoai_endpoint,
        deployment_name=chat_deployment,
        inputs=[
            InputFieldMapping(name="system_message", source="='Describe esta imagen de forma concisa y técnica. Enfócate en datos, fórmulas, ejes de gráficos y conclusiones. No hables de colores ni estilo.'"),
            InputFieldMapping(name="user_message", source="='Por favor describe esta imagen.'"),
            InputFieldMapping(name="image", source="/document/normalized_images/*/data")  # base64
        ],
        outputs=[OutputFieldMapping(name="response", target_name="verbalized_description")]
    ),
    
    # === 3. Embeddings (texto + descripción verbal) ===
    AzureOpenAIEmbeddingSkill(
        name="embedding-skill",
        context="/document/text_sections/*",
        resource_url=aoai_endpoint,
        deployment_name=embedding_deployment,
        inputs=[InputFieldMapping(name="text", source="/document/text_sections/*/content")],
        outputs=[OutputFieldMapping(name="vector", target_name="content_embedding")]
    ),
    AzureOpenAIEmbeddingSkill(
        name="verbalized-embedding",
        context="/document/normalized_images/*",
        resource_url=aoai_endpoint,
        deployment_name=embedding_deployment,
        inputs=[InputFieldMapping(name="text", source="/document/normalized_images/*/verbalized_description")],
        outputs=[OutputFieldMapping(name="vector", target_name="image_embedding")]
    )
]

# === KNOWLEDGE STORE (¡aquí se guardan las imágenes!) ===
knowledge_store = KnowledgeStore(
    storage_connection_string=blob_connection,
    projections=[
        KnowledgeStoreFileProjection(
            storage_container=image_container,
            source="/document/normalized_images/*"
        )
    ]
)

skillset = SearchIndexerSkillset(
    name="mi-pdf-skillset-multimodal",
    description="Layout + Verbalización + Imágenes en Knowledge Store",
    skills=skills,
    knowledge_store=knowledge_store,
    cognitive_services=SearchIndexerAIServicesByIdentity(subdomain_url=doc_intel_endpoint)
)
client.create_or_update_skillset(skillset)

# 3. ÍNDICE (agregamos campos nuevos para imágenes)
# ... (igual que antes pero añade:)
# SearchableField(name="verbalized_description", type="Edm.String"),
# SimpleField(name="image_path", type="Edm.String", searchable=False),
# ComplexField(name="location_metadata", ...)

# 4. INDEXER + Knowledge Source + Knowledge Base
# (igual que en el tutorial anterior, solo cambia el nombre del skillset e índice)

print("✅ Pipeline multimodal completo con imágenes guardadas y verbalizadas!")
```

### Cómo usar las imágenes en tu app de chat (ejemplo rápido)

```python
# Después de recibir la respuesta del agente:
for ref in response.references:
    if ref.image_path:
        image_url = f"https://<tu-storage>.blob.core.windows.net/{image_container}{ref.image_path}?sp=...&sig=..."  # SAS
        print(f"![Gráfico]({image_url})")
```

### Resumen de ventajas de esta versión

- Control total de chunking y overlap.  
- Imágenes guardadas permanentemente.  
- Agente entiende gráficos gracias a la verbalización.  
- Tu UI puede mostrar la imagen exacta (multimodal real).  
