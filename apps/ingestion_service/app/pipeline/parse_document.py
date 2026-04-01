"""
Document parsing step.

For the MVP prototype this will be a placeholder.
Later implementations may use:
 - Docling
 - Azure Document Intelligence
"""

from pathlib import Path


def parse_document(file_path: Path):
    print(f"Parsing file: {file_path}")

    # Placeholder output structure
    return {
        "title": file_path.name,
        "content": "Parsed document content placeholder",
    }
