# Planificación actualizada: Docling como fuente de estructura document schema

## ¿Por qué ajustamos el milestone?
- La investigación del `DoclingDocument` reveló que ya expone `body`, `furniture`, `groups` y metadata de layout para cada bloque. Ese contrato significa que **no necesitamos construir la estructura completa desde cero**; Docling nos entrega headings, párrafos, fórmulas, tablas y agrupaciones de layout.
- Por eso el milestone debe enfatizar que el parser ya no es una caja negra que devuelve texto plano: el output enriquecido de Docling será nuestro punto de partida para la normalización y chunking.

## Objetivos refinados para este milestone
1. Consumir `DoclingDocument` y preservar sus nodos (`body`, `furniture`, `groups`) como una representación intermedia.
2. Mapear cada bloque enriquecido (párrafos, figuras, ecuaciones, tablas) a `ContentBlock` con metadata de page, bounding box, confidence y block_type.
3. Mantener la jerarquía propuesta por Docling para guiar la asignación de `Section` y la orquesta del chunking.
4. Solo cuando la estructura disponible no cubra una necesidad específica entraremos con `normalizer.py` para ajustes puntuales (e.g., unificar delimitadores, limpiar whitespace, detectar listados complejos).

## Pasos concretos que vamos a ejecutar
1. **Refactor parser** (`apps/ingestion_service/app/pipeline/docling/parser.py`): recorrer el árbol `DoclingDocument.body` + `groups`, generar bloques tipados y extraer metadata (page, bbox, font, score). Este módulo será la anti-corruption layer antes de nuestro schema.
2. **Enriquecimiento de contenido**: documentar cómo Docling marca tablas, ecuaciones y figuras (Granite, formula items, etc.) para pasarlos directamente al schema con la metadata necesaria.
3. **Plan para chunking**: utilizar la secuencia ordenada de `groups` para agrupar bloques pequeños, mantener ecuaciones con contexto y respetar el tamaño (200–400 tokens), dejando el paso de normalización para correcciones puntuales.
4. **Documentación del flujo**: el milestone y esta propuesta deben reflejar este enfoque, con notas claras sobre qué hace Docling y qué hacemos nosotros después.

## Riesgos y mitigaciones
- **Bloques sin metadata confiable**: definimos metadata mínima (p.ej., `page`, `content`) para que el parser siga operando aun si faltan bounding boxes.
- **Chunking dependiente de `groups`**: describimos un fallback que agrupa por orden si Docling no genera `groups` o `furniture`.
- **Desalineación con el schema**: mantenemos la correspondencia `Docling group → Section` y `item → ContentBlock` documentada.

## Entregables
1. Parser Docling que emite Document/Section/ContentBlock enriquecidos con metadata de layout.  
2. JSON de salida (ya generado) validado contra el schema.  
3. Roadmap del chunker que aprovecha `groups` y token counts.  
4. Documentación actualizada (milestone + esta propuesta).

Una vez validado este plan, implementamos el parser/enrichment y luego avanzamos al chunking y normalización fina. ¿Seguimos con eso?
