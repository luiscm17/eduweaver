
from azure.storage.blob import BlobServiceClient
from app.config.settings import BlobStorageSettings

class BlobStorageAdapter:
    def __init__(self) -> None:
        BlobStorageSettings.get_connection_string()
        BlobStorageSettings.get_container_name()

        conn_str = BlobStorageSettings.get_connection_string()
        assert conn_str is not None
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    def upload_blob(self, blob_name: str, data: bytes) -> None:
        container_name = BlobStorageSettings.get_container_name()
        assert container_name is not None
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(data, overwrite=True)
    
    def download_blob(self, blob_name: str) -> bytes:
        container_name = BlobStorageSettings.get_container_name()
        assert container_name is not None
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        downloader = blob_client.download_blob()
        return downloader.readall()