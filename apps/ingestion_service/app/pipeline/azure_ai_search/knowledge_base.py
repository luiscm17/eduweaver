"""Service for creating and deploying Azure Search knowledge bases."""

from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizerParameters,
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeRetrievalLowReasoningEffort,
    KnowledgeRetrievalOutputMode,
    KnowledgeSourceReference,
)

from app.config.settings import (
    AIModelSettings,
    KnowledgeBaseSettings,
)
from app.indexing.vector_indexer import SearchIndexService


class KnowledgeBaseService:
    """Builds and deploys knowledge bases that wrap a knowledge source."""

    def __init__(self) -> None:
        self._aoai_endpoint = AIModelSettings.get_openai_endpoint()
        self._aoai_key = AIModelSettings.get_api_key()
        self._index_service = SearchIndexService()

    def _build_model(self) -> KnowledgeBaseAzureOpenAIModel:
        azure_params = AzureOpenAIVectorizerParameters(
            resource_url=self._aoai_endpoint,
            deployment_name=AIModelSettings.get_chat_deployment_name(),
            model_name=AIModelSettings.get_model_name(),
            api_key=self._aoai_key,
        )
        return KnowledgeBaseAzureOpenAIModel(
            azure_open_ai_parameters=azure_params,
        )

    def create_and_deploy(self, knowledge_source_name: str) -> None:
        """Create a knowledge base that references the provided knowledge source."""
        model = self._build_model()
        kb = KnowledgeBase(
            name=KnowledgeBaseSettings.get_name(),
            description=KnowledgeBaseSettings.get_description(),
            knowledge_sources=[KnowledgeSourceReference(name=knowledge_source_name)],
            models=[model],
            output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
            retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort(),
            answer_instructions=KnowledgeBaseSettings.get_answer_instructions(),
            retrieval_instructions=KnowledgeBaseSettings.get_retrieval_instructions(),
        )
        client = self._index_service.get_client()
        client.create_or_update_knowledge_base(kb)
