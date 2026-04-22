from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_STORAGE_CONTAINER_NAME: Optional[str] = None

    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: Optional[str] = None
    AZURE_OPENAI_MODEL_NAME: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None

    EMBEDDING_MODEL_NAME: Optional[str] = None
    EMBEDDING_MODEL_DEPLOYMENT_NAME: Optional[str] = None

    AI_SEARCH_ENDPOINT: Optional[str] = None
    AI_SEARCH_KEY: Optional[str] = None
    AI_SEARCH_INDEX_NAME: Optional[str] = None

    AZURE_SEARCH_SKILLSET_NAME: Optional[str] = None
    AZURE_SEARCH_SKILLSET_DESCRIPTION: Optional[str] = None
    AZURE_DOCUMENT_CHUNK_MAX_LENGTH: Optional[int] = None
    AZURE_DOCUMENT_CHUNK_OVERLAP_LENGTH: Optional[int] = None

    AZURE_DOC_INTEL_ENDPOINT: Optional[str] = None
    AZURE_DOC_INTEL_KEY: Optional[str] = None
    AZURE_DOC_INTEL_LAYOUT_MODEL_ID: Optional[str] = None

    AI_PROJECT_RESOURCE_ID: Optional[str] = None
    AI_PROJECT_CONNECTION_NAME: Optional[str] = "rag-mcp-connection"


env = EnvSettings()


class BlobStorageSettings:
    _AZURE_STORAGE_CONNECTION_STRING: Optional[str] = (
        env.AZURE_STORAGE_CONNECTION_STRING
    )
    _AZURE_STORAGE_CONTAINER_NAME = env.AZURE_STORAGE_CONTAINER_NAME

    @classmethod
    def get_connection_string(cls) -> str:
        if not cls._AZURE_STORAGE_CONNECTION_STRING:
            raise ValueError("Azure connection string is not configured.")
        return cls._AZURE_STORAGE_CONNECTION_STRING

    @classmethod
    def get_container_name(cls) -> str:
        if not cls._AZURE_STORAGE_CONTAINER_NAME:
            raise ValueError("Azure container name is not configured.")
        return cls._AZURE_STORAGE_CONTAINER_NAME


class AIModelSettings:
    _AZURE_OPENAI_ENDPOINT: Optional[str] = env.AZURE_OPENAI_ENDPOINT
    _AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: Optional[str] = (
        env.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    )
    _AZURE_OPENAI_MODEL_NAME: Optional[str] = env.AZURE_OPENAI_MODEL_NAME
    _AZURE_OPENAI_API_KEY: Optional[str] = env.AZURE_OPENAI_API_KEY
    _EMBEDDING_MODEL_NAME: Optional[str] = env.EMBEDDING_MODEL_NAME
    _EMBEDDING_MODEL_DEPLOYMENT_NAME: Optional[str] = (
        env.EMBEDDING_MODEL_DEPLOYMENT_NAME
    )

    @classmethod
    def get_openai_endpoint(cls) -> str:
        endpoint = cls._AZURE_OPENAI_ENDPOINT
        if not endpoint:
            raise ValueError("Azure OpenAI Endpoint is not configured.")
        return endpoint

    @classmethod
    def get_chat_deployment_name(cls) -> str:
        deployment = cls._AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
        if not deployment:
            raise ValueError("Azure OpenAI Chat Deployment Name is not configured.")
        return deployment

    @classmethod
    def get_model_name(cls) -> str:
        model = cls._AZURE_OPENAI_MODEL_NAME
        if not model:
            raise ValueError("Azure OpenAI Model Name is not configured.")
        return model

    @classmethod
    def get_api_key(cls) -> str:
        key = cls._AZURE_OPENAI_API_KEY
        if not key:
            raise ValueError("Azure OpenAI API Key is not configured.")
        return key

    @classmethod
    def get_embedding_deployment_name(cls) -> str:
        embedding_deployment_name = cls._EMBEDDING_MODEL_DEPLOYMENT_NAME
        if not embedding_deployment_name:
            raise ValueError("EMBEDDING_MODEL_DEPLOYMENT_NAME is not configured")
        return embedding_deployment_name

    @classmethod
    def get_embedding_model_name(cls) -> str:
        embedding_model_name = cls._EMBEDDING_MODEL_NAME
        if not embedding_model_name:
            raise ValueError("EMBEDDING_MODEL_NAME is not configured")
        return embedding_model_name


class DocumentIntelligenceSettings:
    """Shared configuration for Document Intelligence integrations."""

    _DOC_INTEL_ENDPOINT: Optional[str] = env.AZURE_DOC_INTEL_ENDPOINT
    _DOC_INTEL_KEY: Optional[str] = env.AZURE_DOC_INTEL_KEY
    _DOC_INTEL_LAYOUT_MODEL_ID: Optional[str] = env.AZURE_DOC_INTEL_LAYOUT_MODEL_ID

    @classmethod
    def get_endpoint(cls) -> str:
        endpoint = cls._DOC_INTEL_ENDPOINT
        if not endpoint:
            raise ValueError("AZURE_DOC_INTEL_ENDPOINT is not configured")
        return endpoint

    @classmethod
    def get_key(cls) -> str:
        key = cls._DOC_INTEL_KEY
        if not key:
            raise ValueError("AZURE_DOC_INTEL_KEY is not configured")
        return key

    @classmethod
    def get_layout_model_id(cls) -> str:
        return cls._DOC_INTEL_LAYOUT_MODEL_ID or "prebuilt-layout"


class SkillsetSettings:
    """Configuration helpers for the Azure Search skillset."""

    _SKILLSET_NAME: Optional[str] = env.AZURE_SEARCH_SKILLSET_NAME
    _SKILLSET_DESCRIPTION: Optional[str] = env.AZURE_SEARCH_SKILLSET_DESCRIPTION
    _CHUNK_MAX: Optional[int] = env.AZURE_DOCUMENT_CHUNK_MAX_LENGTH
    _CHUNK_OVERLAP: Optional[int] = env.AZURE_DOCUMENT_CHUNK_OVERLAP_LENGTH

    @classmethod
    def get_name(cls) -> str:
        return cls._SKILLSET_NAME or "eduweaver-document-layout-skillset"

    @classmethod
    def get_description(cls) -> str:
        return (
            cls._SKILLSET_DESCRIPTION
            or "Document Intelligence + embeddings para EduWeaver."
        )

    @classmethod
    def get_chunk_max_length(cls) -> int:
        return cls._CHUNK_MAX or 2000

    @classmethod
    def get_chunk_overlap_length(cls) -> int:
        return cls._CHUNK_OVERLAP or 200


class AISearchSettings:
    _AI_SEARCH_ENDPOINT: Optional[str] = env.AI_SEARCH_ENDPOINT
    _AI_SEARCH_API_KEY: Optional[str] = env.AI_SEARCH_KEY
    _AI_SEARCH_INDEX_NAME: Optional[str] = env.AI_SEARCH_INDEX_NAME

    @classmethod
    def get_endpoint(cls) -> str:
        """Retrieve the Azure Search endpoint from environment."""
        ai_search_endpoint = cls._AI_SEARCH_ENDPOINT
        if not ai_search_endpoint:
            raise ValueError("AI_SEARCH_ENDPOINT is not configured")
        return ai_search_endpoint

    @classmethod
    def get_api_key(cls) -> str:
        """Retrieve the Azure Search API key from environment."""
        ai_search_key = cls._AI_SEARCH_API_KEY
        if not ai_search_key:
            raise ValueError("AI_SEARCH_KEY is not configured")
        return ai_search_key

    @classmethod
    def get_index_name(cls) -> str:
        """Retrieve the Azure Search index name from environment."""
        ai_search_name = cls._AI_SEARCH_INDEX_NAME
        if not ai_search_name:
            raise ValueError("AI_SEARCH_INDEX_NAME is not configured")
        return ai_search_name


class KnowledgeSourceSettings:
    """Centralized settings for the default knowledge source."""

    _KS_NAME = "default-knowledge-source"
    _KS_DESCRIPTION = "Knowledge source created from documents stored in blob storage"

    @classmethod
    def _value_or_default(cls, value: Optional[str], default: str) -> str:
        resolved = value or default
        if not resolved.strip():
            raise ValueError("Knowledge source values must not be empty")
        return resolved

    @classmethod
    def get_name(cls) -> str:
        """Return the configured knowledge source name."""
        return cls._KS_NAME

    @classmethod
    def get_description(cls) -> str:
        """Return the configured knowledge source description."""
        return cls._KS_DESCRIPTION

    @classmethod
    def validate(cls) -> None:
        """Ensure both name and description are resolvable."""
        cls.get_name()
        cls.get_description()


class KnowledgeBaseSettings:
    """Centralized settings for the default knowledge base."""

    _KB_NAME = "default-knowledge-base"
    _KB_DESCRIPTION = (
        "Retrieval augmented knowledge base built from indexed document content"
    )
    _KB_ANSWER_INSTRUCTIONS = (
        "Answer using retrieved context only. Cite document page. No fabrication."
    )
    _KB_RETRIEVAL_INSTRUCTIONS = "Use most relevant retrieved passages. Prefer accuracy. Reference document page when available."

    @classmethod
    def _value_or_default(cls, value: Optional[str], default: str) -> str:
        resolved = value or default
        if not resolved.strip():
            raise ValueError("Knowledge base values must not be empty")
        return resolved

    @classmethod
    def get_name(cls) -> str:
        return cls._KB_NAME

    @classmethod
    def get_description(cls) -> str:
        return cls._KB_DESCRIPTION

    @classmethod
    def get_answer_instructions(cls) -> str:
        return cls._KB_ANSWER_INSTRUCTIONS

    @classmethod
    def get_retrieval_instructions(cls) -> str:
        return cls._KB_RETRIEVAL_INSTRUCTIONS

    @classmethod
    def validate(cls) -> None:
        cls.get_name()
        cls.get_description()
        cls.get_answer_instructions()
        cls.get_retrieval_instructions()


class MCPConnectionSettings:
    """Configuration for exposing the knowledge base as an MCP tool."""

    _PROJECT_RESOURCE_ID: Optional[str] = env.AI_PROJECT_RESOURCE_ID
    _PROJECT_CONNECTION_NAME: Optional[str] = env.AI_PROJECT_CONNECTION_NAME

    @classmethod
    def get_project_resource_id(cls) -> str:
        resource_id = cls._PROJECT_RESOURCE_ID
        if not resource_id:
            raise ValueError("AI_PROJECT_RESOURCE_ID is not configured")
        return resource_id

    @classmethod
    def get_project_connection_name(cls) -> str:
        connection_name = cls._PROJECT_CONNECTION_NAME
        if not connection_name:
            raise ValueError("PROJECT_CONNECTION_NAME is not configured")
        return connection_name

    @classmethod
    def get_project_connection_id(cls) -> str:
        resource_id = cls.get_project_resource_id()
        connection_name = cls.get_project_connection_name()
        return f"{resource_id}/connections/{connection_name}"

    @classmethod
    def get_mcp_endpoint(cls) -> str:
        search_endpoint = AISearchSettings.get_endpoint()
        kb_name = KnowledgeBaseSettings.get_name()
        return f"{search_endpoint}/knowledgebases/{kb_name}/mcp?api-version=2025-11-01-Preview"
