"""
Ingestion Service Entry Point

Initial prototype for Milestone 01.

Pipeline:
PDF -> Parse -> Normalize -> Chunk -> Embed -> Index

This version runs as a local script for development and testing.
"""

import sys
from pathlib import Path

from apps.ingestion_service.app.pipeline.parse_document import parse_document
from apps.ingestion_service.app.pipeline.normalize_document import normalize_document
from apps.ingestion_service.app.pipeline.chunk_document import chunk_document
from apps.ingestion_service.app.pipeline.generate_embeddings import generate_embeddings
from apps.ingestion_service.app.indexing.vector_indexer import index_chunks


def run_pipeline(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    print("\n--- Ingestion Pipeline Started ---")

    print("[1] Parsing document...")
    parsed = parse_document(path)

    print("[2] Normalizing document structure...")
    normalized = normalize_document(parsed)

    print("[3] Creating semantic chunks...")
    chunks = chunk_document(normalized)

    print("[4] Generating embeddings...")
    embedded_chunks = generate_embeddings(chunks)

    print("[5] Indexing chunks in vector database...")
    index_chunks(embedded_chunks)

    print("--- Ingestion Pipeline Completed ---\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <document_path>")
        sys.exit(1)

    run_pipeline(sys.argv[1])
