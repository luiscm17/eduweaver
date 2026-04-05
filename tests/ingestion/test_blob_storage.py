import io
import os
import sys

import pytest

# Ensure repository root is available for absolute imports like `apps.*`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from apps.ingestion_service.app.adapters.blob_storage import BlobStorageAdapter
import apps.ingestion_service.app.adapters.blob_storage as adapter_module
from apps.ingestion_service.app.config import credentials
from apps.ingestion_service.app.config.settings import BlobStorageSettings


@pytest.fixture(autouse=True)
def reset_blob_settings(monkeypatch):
    monkeypatch.setattr(
        BlobStorageSettings, "_AZURE_STORAGE_CONNECTION_STRING", "conn-str"
    )
    monkeypatch.setattr(
        BlobStorageSettings, "_AZURE_STORAGE_CONTAINER_NAME", "container"
    )
    return


def test_create_blob_service_client(monkeypatch):
    calls = []

    class _Fake:
        @staticmethod
        def from_connection_string(value):
            calls.append(value)
            return "client"

    monkeypatch.setattr(credentials, "BlobServiceClient", _Fake)

    service = credentials.create_blob_service_client()

    assert service == "client"
    assert calls == ["conn-str"]


def test_get_blob_client(monkeypatch):
    blob_clients = []

    class FakeService:
        def get_blob_client(self, container, blob):
            blob_clients.append((container, blob))
            return "blob-client"

    monkeypatch.setattr(
        credentials, "create_blob_service_client", lambda: FakeService()
    )

    blob = credentials.get_blob_client("doc.pdf")

    assert blob == "blob-client"
    assert blob_clients == [("container", "doc.pdf")]


def test_download_blob_stream(monkeypatch):
    class FakeDownloader:
        def readinto(self, stream):
            stream.write(b"data")

    class FakeBlob:
        def download_blob(self):
            return FakeDownloader()

    monkeypatch.setattr(credentials, "get_blob_client", lambda name: FakeBlob())

    stream = credentials.download_blob_stream("doc.pdf")

    assert isinstance(stream, io.BytesIO)
    assert stream.read() == b"data"


def test_list_blob_names(monkeypatch):
    class FakeContainer:
        def list_blobs(self):
            return [
                type("B", (), {"name": "a.pdf"})(),
                type("B", (), {"name": "b.pdf"})(),
            ]

    class FakeService:
        def get_container_client(self, container):
            assert container == "container"
            return FakeContainer()

    monkeypatch.setattr(
        credentials, "create_blob_service_client", lambda: FakeService()
    )

    names = list(credentials.list_blob_names())

    assert names == ["a.pdf", "b.pdf"]


def test_blob_adapter_list_and_stream(monkeypatch):
    names = ["a.pdf", "b.pdf"]
    monkeypatch.setattr(adapter_module, "list_blob_names", lambda: iter(names))
    monkeypatch.setattr(
        adapter_module,
        "download_blob_stream",
        lambda blob_name: io.BytesIO(blob_name.encode()),
    )

    adapter = BlobStorageAdapter()

    assert list(adapter.list_blobs()) == names
    assert adapter.open_stream("a.pdf").read() == b"a.pdf"
