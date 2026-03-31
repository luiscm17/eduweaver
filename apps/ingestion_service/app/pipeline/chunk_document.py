"""
Chunking step.

Converts content blocks into semantic chunks suitable for RAG.
"""


def chunk_document(normalized_document):
    print("Chunking document")

    return [
        {
            "chunk_id": "chunk_1",
            "content": "Example chunk content",
        }
    ]
