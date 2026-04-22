Dale, hermanito, me puse a investigar a fondo los dos docs que mencionaste y acá va el reporte con evidencia oficial y sugerencias. Lo armé en Markdown como pediste, con secciones claras, referencias a la doc de Azure y verificación de los snippets.

# Investigación multimodal RAG (raspado de docs/rag-v2.md y rag-v3.md)

## 1. Objetivo

Verificar que el enfoque manual de multimodal RAG que proponés en `rag-v2.md` y el pipeline de Knowledge Store + verbalización en `rag-v3.md` estén alineados con la documentación oficial de Azure (AI Search, Document Intelligence y Agent Framework) y que los fragmentos de código referencien SDK/clases válidas
---

## 2. Confirmaciones clave

### a) Chunking inteligente con Document Layout Skill (v2)

- **Qué dice el doc:** El skill extrae texto, imágenes y `locationMetadata`, controla chunk size/overlap y preserva estructuras complejas.
- **Verificación:** La doc oficial del skill (`https://learn.microsoft.com/azure/search/cognitive-search-skill-document-intelligence-layout#skill-outputs`) confirma que:
  - Se puede usar `output_format="text"` para obtener `text_sections` y `normalized_images`.
  - `locationMetadata` viene incluido en los chunks si se habilita, y los campos `boundingPolygon` / `pageNumber` están disponibles.
  - El chunking se controla mediante `chunking_properties` (último ejemplo en la doc).
- **Resultado:** ✅ El enfoque está correcto. El código usa `DocumentIntelligenceLayoutSkill` con `chunking_properties` y `extraction_options=["images","locationMetadata"]`, que es exactamente lo que la doc describe.

### b) Hacer embeddings con AzureOpenAIEmbeddingSkill (v2)

- **Qué dice:** Se agregan embedding para cada chunk textual.
- **Verificación:** Los SDK (referente `AzureOpenAIEmbeddingSkill` y `TextSplitSkill`) son parte del modelo `azure.search.documents.indexes.models` y el uso de `deployment_name` + `resource_url` es conforme a los ejemplos oficiales (`https://learn.microsoft.com/azure/search/cognitive-search-skill-azure-openai-embedding`).
- **Resultado:** ✅ El snippet es válido, se crean vectores por chunk y el índice puede configurar `vector_search` con HNSW (como se hace en el doc).

### c) Inclusión de imágenes en Knowledge Store + verbalización (v3)

- **Qué dice:** Knowledge Store guarda las imágenes normalizadas, `imagePath` da la ruta, y un skill llama a Azure OpenAI Vision/Chat para describirlas.
- **Verificación:**
  - La doc Multimodal (`https://learn.microsoft.com/azure/search/tutorial-multimodal#run-queries`) explica que los normalized images se proyectan a Blob, el campo `content_path`/`imagePath` aparece en la metadata y se usa para construir URLs.
  - La doc del Document Layout skill menciona explícitamente el output `imagePath` y `normalized_images` (`https://learn.microsoft.com/azure/search/cognitive-search-skill-document-intelligence-layout#skill-outputs`).
  - Las instrucciones sobre el acceso a Blob (SAS, Storage SDK) y que el agente sólo usa texto están alineadas con el tutorial (`https://learn.microsoft.com/azure/search/tutorial-multimodal#run-queries`) donde dicen “no puedes devolver imágenes en la API de búsqueda, pero tu app puede descargarlas”.
  - La verbalización con `AzureOpenAIChatCompletionSkill` y posterior embedding es un patrón documentado en el tutorial multimodal (`https://learn.microsoft.com/azure/search/tutorial-multimodal#set-up-a-pipeline`), donde recomiendan uno o dos skills adicionales (GenAI Prompt o ChatCompletion) para describir imágenes/diagramas y luego vectorizar ese texto.
- **Resultado:** ✅ La narrativa y el código de `rag-v3.md` están correctos y cuadran con la doc oficial: Knowledge Store almacena las imágenes y el agente trabaja con descripciones textuales enriquecidas.

### d) Consideraciones de Agent Framework y Knowledge Base

- **Qué dice `rag-v2.md`:** Después de la colección de chunks se crea un índice, knowledge source/knowledge base y se usa `KnowledgeBaseRetrievalClient`.
- **Verificación:** Los nombres de clases (`KnowledgeBase`, `KnowledgeSourceReference`, `KnowledgeBaseAzureOpenAIModel`, etc.) son oficiales del SDK (`https://learn.microsoft.com/azure/search/search-knowledge-base-overview` y `https://learn.microsoft.com/azure/search/tutorial-knowledge-base`). Ese flujo sigue los ejemplos del tutorial “Manual agentic RAG”.
- **Resultado:** ✅ El código existe y las clases son válidas.

---

## 3. Hallazgos y recomendaciones

1. **Evitar llaves expuestas**: los ejemplos usan `AzureKeyCredential` + strings hardcodeadas. En producción, es mejor pasar por Managed Identity o `DefaultAzureCredential` (como ya aplicaste en el resto del repo) para seguridad, especialmente en pipeline de ingestión.
2. **Verbalización detallada**: el skill `AzureOpenAIChatCompletionSkill` debe recibir prompts claros (como los propuestos) y idealmente limitar tokens/resumen para evitar costos. Podés mencionar esto en la doc para el equipo.
3. **Uso de `locationMetadata`/`imagePath` en UI**: la sección que explica cómo renderizar las imágenes en la app con SAS está alineada con la doc; conviene mostrar un ejemplo completo (con `get_blob_sas_token`) para que no queden dudas.
4. **Auditoría de costos**: la doc debería incluir un recordatorio de que los skills que llaman a Document Intelligence y Azure OpenAI Vision consumen Foundry, por si quieren medir presupuesto.

---

## 4. Conclusión

La investigación está bien encuadrada: los pipeline propuestos en `rag-v2.md` y `rag-v3.md` reflejan exactamente lo que la documentación oficial de Azure AI Search, Document Intelligence y Agent Framework recomienda para lidiar con PDFs complejos y contenido multimodal. Los códigos referencian clases reales, los pasos de Knowledge Store / embeddings / verbalización están respaldados por los ejemplos oficiales y la narrativa sobre cómo el UI consume las imágenes es correcta. La única mejora inmediata: reforzar la parte de seguridad (credentials) y añadir notas de costos/limitaciones de Foundry.
Si te parece, puedo pulir esos docs con anotaciones (ej. enlaces directos, recordatorios de credenciales seguras, ejemplos de SAS) o convertir esto en una propuesta con recomendaciones claras. ¿Querés que lo documente como PR o lo dejamos como investigación enriquecida?
