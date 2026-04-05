"""Service for creating and ingesting Azure Blob Knowledge Sources."""

from azure.search.documents.indexes.models import (
    AzureBlobKnowledgeSource,
    AzureBlobKnowledgeSourceParameters,
    KnowledgeSourceIngestionParameters,
    KnowledgeSourceContentExtractionMode,
    KnowledgeBaseAzureOpenAIModel,
    AzureOpenAIVectorizerParameters,
    KnowledgeSourceAzureOpenAIVectorizer,
)

from apps.ingestion_service.app.config.settings import (
    BlobStorageSettings,
    AISearchSettings,
    AIModelSettings,
)
from apps.ingestion_service.app.indexing.vector_indexer import SearchIndexService


class KnowledgeSourceService:
    """Service to build and ingest AzureBlobKnowledgeSource instances."""

    def __init__(self) -> None:
        self._index_service = SearchIndexService()

        self._aoai_endpoint = AIModelSettings.get_openai_endpoint()
        self._aoai_key = AIModelSettings.get_api_key()
        self._embedding_name = AIModelSettings.get_embedding_model_name()
        self._embedding_deployment_name = (
            AIModelSettings.get_embedding_deployment_name()
        )

    def create_knowledge_source(
        self, container_name: str, description: str
    ) -> AzureBlobKnowledgeSource:
        embedding_params = AzureOpenAIVectorizerParameters(
            resource_url=self._aoai_endpoint,
            deployment_name=AIModelSettings.get_embedding_deployment_name(),
            model_name=AIModelSettings.get_embedding_model_name(),
            api_key=self._aoai_key,
        )

        chat_params = AzureOpenAIVectorizerParameters(
            resource_url=self._aoai_endpoint,
            deployment_name=AIModelSettings.get_chat_deployment_name(),
            model_name=AIModelSettings.get_chat_deployment_name(),
            api_key=self._aoai_key,
        )

        ingestion_params = KnowledgeSourceIngestionParameters(
            identity=None,
            disable_image_verbalization=False,
            content_extraction_mode=KnowledgeSourceContentExtractionMode.MINIMAL,
            embedding_model=KnowledgeSourceAzureOpenAIVectorizer(
                azure_open_ai_parameters=embedding_params
            ),
            chat_completion_model=KnowledgeBaseAzureOpenAIModel(
                azure_open_ai_parameters=chat_params
            ),
            ingestion_schedule=None,
            ingestion_permission_options=None,
        )

        blob_params = AzureBlobKnowledgeSourceParameters(
            connection_string=BlobStorageSettings.get_connection_string(),
            container_name=BlobStorageSettings.get_container_name(),
            is_adls_gen2=False,
            ingestion_parameters=ingestion_params,
        )

        return AzureBlobKnowledgeSource(
            name=container_name,
            description=description,
            azure_blob_parameters=blob_params,
        )

    def ingest(self, ks: AzureBlobKnowledgeSource) -> None:
        client = self._index_service.get_client()
        client.create_or_update_knowledge_source(ks)
