"""Helper utilities to create Azure Blob clients and access blobs."""

from io import BytesIO
from typing import Iterator

from azure.storage.blob import BlobServiceClient, BlobClient

from apps.ingestion_service.app.config.settings import BlobStorageSettings


def create_blob_service_client() -> BlobServiceClient:
    """Return an authenticated BlobServiceClient using configured settings."""
    connection_string = BlobStorageSettings.get_connection_string()
    return BlobServiceClient.from_connection_string(connection_string)


def get_blob_client(blob_name: str) -> BlobClient:
    """Return a BlobClient for the configured container and the given blob."""
    service_client = create_blob_service_client()
    container_name = BlobStorageSettings.get_container_name()
    return service_client.get_blob_client(container=container_name, blob=blob_name)


def download_blob_stream(blob_name: str) -> BytesIO:
    """Download the blob content into an in-memory stream."""
    blob_client = get_blob_client(blob_name)
    downloader = blob_client.download_blob()
    stream = BytesIO()
    downloader.readinto(stream)
    stream.seek(0)
    return stream


def list_blob_names() -> Iterator[str]:
    """Yield each blob name from the configured container."""
    service_client = create_blob_service_client()
    container_name = BlobStorageSettings.get_container_name()
    container_client = service_client.get_container_client(container=container_name)
    for blob in container_client.list_blobs():
        yield blob.name
