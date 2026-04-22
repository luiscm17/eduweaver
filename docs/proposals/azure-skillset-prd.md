# PRD: Skillset rollout para RAG sobre Azure

Fecha: 2026-04-12
Status: Draft

## 1. Propósito
Formalizar qué skillsets y recursos Azure debemos aprovisionar para el pipeline de RAG que ya definimos en `rag-v2.md` / `rag-v3.md` y así tener una hoja de ruta clara antes de tocar la implementación. El PRD define quién consume qué, qué datos fluyen por el pipeline y cuáles son los criterios mínimos de aceptación para considerar el componente listo.

## 2. Contexto

- En esta rama estamos construyendo el RAG de Azure Cloud; Docling es un pipeline paralelo y no lo mezclamos.
- Ya tenemos el código para crear la `Knowledge Source`, `Knowledge Base` y conexión MCP (docs/implementation/mvp-milestone-01-ingestion y `apps/ingestion_service`).
- Las propuestas `rag-v2.md` y `rag-v3.md` muestran la arquitectura ideal: Document Intelligence Manual + skillset controlado + knowledge store + verbalización.

## 3. Alcance para esta fase

### Objetivos principales
1. Definir oficialmente la estructura del pipeline Azure: flujo de datos, qué parte controla EduWeaver y qué queda en Azure Search.
2. Documentar qué skillsets vamos a crear y cómo se relacionan con los recursos existentes (Blob Storage, Document Intelligence, Azure Search, Knowledge Base).
3. Establecer criterios de aceptación, dependencias y riesgos antes de escribir código o scripts de provisioning.

### Recursos a aprovisionar

| Recurso | Descripción | Responsable |
| --- | --- | --- |
| **Azure Document Intelligence endpoint** | Procesa PDFs para extraer párrafos, tablas, imágenes y locationMetadata. Requerido por el skillset principal. | Infra/Cloud dev |
| **Blob Storage (contenedor de PDFs)** | Origen de los documentos. Debe permitir SAS o Managed Identity para que Azure Search/Doc Intelligence los descargue. | Infra/Cloud dev + Equipo RAG |
| **Search Index + Vector fields** | Índice con campos: `id`, `content`, `content_embedding`, `page_number`, `locationMetadata`, `imagePath`, `verbalized_description`, `document_title`. Debe incluir VectorSearch profile (HNSW). | Equipo backend |
| **Skillset manual (Document Layout Skill + embeddings)** | Document Layout Skill con chunking controlado, extracción de imágenes y outputs `text_sections` + `normalized_images`. Skills adicionales para embeddings y verbalización (ver `rag-v3`). | Equipo backend |
| **Knowledge Store** | Guarde los assets normalizados e imágenes. Deje `imagePath` disponible para la UI. | Equipo backend |
| **Indexer y CI/CD** | Indexer que combine data source, skillset y search index, con field mappings para metadatos. | Equipo backend |
| **Knowledge Source + Knowledge Base** | Ya existen los servicios; se debe verificar que apunten al índice creado. | Equipo backend |

### Flujo esperado (mvp)

1. EduWeaver sube PDFs al Blob Storage (usa `BlobStorageAdapter`).
2. El Document Layout Skill (Document Intelligence) extrae texto/imágenes, chunking y locationMetadata.
3. Azure OpenAI embedding skill genera vectores de `text_sections`; chat completion skill verbaliza las imágenes.
4. Knowledge Store guarda imágenes y produce `imagePath` + `locationMetadata`.
5. Indexer empuja los datos a `SearchIndex` configurado para vector search.
6. `KnowledgeSourceService`/`KnowledgeBaseService` se aseguran de que el agente use ese índice.

## 4. Detalles de implementación

### 4.1 Variables de entorno y credenciales

- `AZURE_DOC_INTEL_ENDPOINT` y `AZURE_DOC_INTEL_KEY`: puntos de entrada a Document Intelligence. El skillset debe usar credenciales distintas al Search Index si se alojan en otro recurso.
- `AZURE_DOC_INTEL_MODEL` (o `AZURE_DOC_INTEL_DEPLOYMENT`): modelo/layout que se usará para chunking y extracción de imágenes.
- Los valores anteriores se consumen desde `apps/ingestion_service/app/config/settings.py`, extendiendo el `EnvSettings` actual y agregando helpers como `DocumentIntelligenceSettings.get_endpoint()`.
- Conservamos los env vars existentes (`AZURE_STORAGE_CONNECTION_STRING`, `AI_SEARCH_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, etc.) y documentamos en `.env.example` cómo combinarlos con las nuevas variables.

### 4.2 Estructura de archivos y módulos

- `apps/ingestion_service/app/pipeline/azure_ai_search/` debe crecer para incluir:
  - `skillset.py`: crea la definición completa del skillset (Document Layout, embeddings, verbalización e instrucciones para `locationMetadata`).
  - `index.py`: define campo `vector_search`, `SimpleField` y `SearchField` necesarios, y expone un helper `create_or_update_index()`.
  - `indexer.py`: arma el `SearchIndexer` y `SearchIndexerDataSourceConnection`, ejecuta `run_indexer` y expone status.
  - `document_intelligence.py`: encapsula cualquier transformación local que necesitemos (por ejemplo, validar que el blob está listo antes de correr el indexer).
  - `knowledge_store.py`: define las proyecciones para guardar imágenes, la container para los assets generados y las rutas resultantes (`imagePath`).
- `apps/ingestion_service/app/adapters/blob_storage.py` sigue siendo la única entrada a los blobs; hay que documentar cómo se usan con el skillset (nombres de blobs, rutas, `metadata_storage_path`).
- `apps/ingestion_service/app/main.py` mantiene el orquestador (`run_pipeline`), pero debemos permitirle: (a) crear el índice + skillset si no existen, (b) crear/actualizar data source, (c) ejecutar el indexer y (d) desplegar KB + MCP connection.
- Documentar la nueva carpeta `docs/azure-skillset/` (si la creamos) con diagramas y ejemplos de comandos `uv run python -m ...`.

### 4.3 Flujo de despliegue manual

- Aprovisionar Document Intelligence en Azure Portal (usuario lo hará manual). Registrar `endpoint` + `key` en `.env`.
- Crear el Blob Storage container y subir documentos de prueba (PDFs complejos).
- Ejecutar `uv run python -m apps.ingestion_service.app.main` para que cree los recursos (index, skillset, indexer, knowledge base). Validar manualmente en Azure Portal que el skillset se ejecutó sin errores.
- Una vez aprobado, documentar el comando concreto para disparar el indexer (`indexer_client.run_indexer(...)`) y la ruta para consultar la KB.

### 4.4 Documentación y QA

- Actualizar `docs/implementation/mvp-milestone-01-ingestion.md` y/o crear un README específico bajo `apps/ingestion_service/` explicando:
  - Cómo configurar el `.env` con las nuevas credenciales Document Intelligence.
  - Cómo correr `run_pipeline` y cómo inspeccionar las imágenes guardadas (`imagePath`).
  - Qué logs buscar para confirmar que el skillset generó `locationMetadata` y `imagePath`.
- Añadir un test manual definido (podría ser un checklist) con pasos para ejecutar el indexer, verificar que el índice contiene `content_embedding` y ejecutar un query de prueba.

## 5. Criterios de aceptación

1. El skillset puede ejecutarse (document layout + embeddings/verbalización) y genera los campos descritos.
2. El índice definido existe en Azure Search con vector search habilitado y campos `locationMetadata` e `imagePath`.
3. Las imágenes verbalizadas quedan disponibles para que la UI las consuma vía `imagePath` + SAS/Managed Identity.
4. Ejecutamos un query de prueba (`"Explica la ecuación ROP"`) y la Knowledge Base retorna chunk + metadatos (página, locationMetadata, imagePath). Se documenta el comando.
5. Si el skillset falla se registra la falla y se describe qué módulo está incompleto (Document Intelligence, embeddings, indexer, knowledge store).

## 6. Dependencias / bloqueos

- Document Intelligence se desplegará manualmente (sin Terraform). Registrar el procedimiento y las credenciales en `.env`.
- Infraestructura de Azure Search (endpoint, índices, knowledge store) se gestiona con scripts Python + CLI; documentar los comandos exactos para crear el índice y el skillset.
- Documentación y pruebas de acceso a las imágenes guardadas.

## 7. Riesgos importantes

1. **Costos de Document Intelligence + embeddings**: Document Layout Skill + AzureOpenAIEmbeddingSkill atacan Foundry; monitorear el uso durante pruebas.
2. **Sincronización de metadatos**: si el skillset no escribe `locationMetadata` o `imagePath`, el agente pierde contexto de imágenes. Hay que validar la configuración del skillset con Azure Portal.
3. **Fallas en la ingesta manual**: la pipeline manual es más frágil que el flujo automático. Debemos documentar pasos de recuperación (reindexar, limpiar blobs temporales).

## 8. Próximos pasos sugeridos

1. Validar manualmente (sin Terraform) las credenciales necesarias para Document Intelligence y Azure Search. Registrar los pasos en un archivo de operaciones.
2. Crear scripts Python/CLI para crear el Search Index + skillset + indexer (basado en `rag-v2`/`rag-v3`) y documentar los comandos concretos para ejecutarlos.
3. Actualizar `apps/ingestion_service` con la lógica de upgrade: helpers que crean el índice si no existe y otro que ejecuta el indexer y reporta el estado.
4. Documentar el flujo de QA: cómo ejecutar el indexer manualmente, cómo verificar `imagePath` y `locationMetadata` en el portal, y cómo interrogar la KB.
5. Preparar un checklist de pruebas (ingestión, retrieval, UI) y un comando de validación (`"Explica la ecuación ROP"`).

## 9. Referencias

- `docs/proposals/rag-v2.md`
- `docs/proposals/rag-v3.md`
- `docs/implementation/mvp-milestone-01-ingestion.md`
- `apps/ingestion_service/app/main.py`
- `apps/ingestion_service/app/pipeline/azure_ai_search/*`
