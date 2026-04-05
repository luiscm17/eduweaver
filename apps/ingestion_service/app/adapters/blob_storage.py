from io import BytesIO
from typing import Iterator

from azure.storage.blob import BlobClient

from app.config.credentials import (
    download_blob_stream,
    get_blob_client,
    list_blob_names,
)


class BlobStorageAdapter:
    """Adapter that exposes Azure Blob operations required by ingestion pipelines."""

    def list_blobs(self) -> Iterator[str]:
        """Yield every blob name that resides in the configured container."""
        yield from list_blob_names()

    def open_stream(self, blob_name: str) -> BytesIO:
        """Return a binary stream of the requested blob."""
        return download_blob_stream(blob_name)

    def get_blob_reference(self, blob_name: str) -> BlobClient:
        """Return a BlobClient reference to perform advanced operations."""
        return get_blob_client(blob_name)
