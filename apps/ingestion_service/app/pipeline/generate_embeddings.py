"""
Embedding generation step.

This will later call an embedding model (OpenAI/Azure/local).
"""


def generate_embeddings(chunks):
    print("Generating embeddings")

    for chunk in chunks:
        chunk["embedding"] = [0.0] * 10

    return chunks
