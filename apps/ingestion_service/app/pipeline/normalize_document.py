"""
Normalization step.

Transforms parsed output into the internal document schema.
"""


def normalize_document(parsed_document):
    print("Normalizing document structure")

    return {
        "document": parsed_document,
        "sections": [],
        "content_blocks": [],
    }
