import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class BlobStorageSettings:
    _AZURE_STORAGE_CONNECTION_STRING: Optional[str]=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    _AZURE_STORAGE_CONTAINER_NAME=os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    @classmethod
    def get_connection_string(cls) -> None:
        if not cls._AZURE_STORAGE_CONNECTION_STRING:
            raise ValueError("Azure String is not configured.")
        
    @classmethod
    def get_container_name(cls) -> None:
        if not cls._AZURE_STORAGE_CONTAINER_NAME:
            raise ValueError("Azure Container Name is not configured.")

class AIModelSettings:
    _AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    _AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: Optional[str] = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    _AZURE_OPENAI_MODEL_NAME: Optional[str] = os.getenv("AZURE_OPENAI_MODEL_NAME")
    _AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    _EMBEDDING_MODEL_NAME: Optional[str] = os.getenv("EMBEDDING_MODEL_NAME")
    _EMBEDDING_MODEL_DEPLOYMENT_NAME: Optional[str] = os.getenv(
        "EMBEDDING_MODEL_DEPLOYMENT_NAME"
    )

    @classmethod
    def get_openai_endpoint(cls) -> None:
        if not cls._AZURE_OPENAI_ENDPOINT:
            raise ValueError("Azure OopenAI Endpoint is not configured.")
        
    @classmethod
    def get_chat_deployment_name(cls) -> None:
        if not cls._AZURE_OPENAI_CHAT_DEPLOYMENT_NAME:
            raise ValueError("Azure OpenAI Chat Deployment Name is not Configured.")
        
    @classmethod
    def get_model_name(cls) -> None:
        if not cls._AZURE_OPENAI_MODEL_NAME:
            raise ValueError("Azure OpenAI Model Name is not configured.")
        
    @classmethod
    def get_api_key(cls) -> None:
        if not cls._AZURE_OPENAI_API_KEY:
            raise ValueError("Azure OpenAI API Key is not configured.")
    
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
        
class AISearchSettings:
    _AI_SEARCH_ENDPOINT: Optional[str] = os.getenv("AI_SEARCH_ENDPOINT")
    _AI_SEARCH_API_KEY: Optional[str] = os.getenv("AI_SEARCH_KEY")
    _AI_SEARCH_INDEX_NAME: Optional[str] = os.getenv("AI_SEARCH_INDEX_NAME")


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

    _KS_DEFAULT_NAME = "ks-name-default"
    _KS_DEFAULT_DESCRIPTION = "Knowledge Source automática desde Blob con mi PDF"
    _KS_NAME: Optional[str] = os.getenv("KNOWLEDGE_SOURCE_NAME")
    _KS_DESCRIPTION: Optional[str] = os.getenv("KNOWLEDGE_SOURCE_DESCRIPTION")

    @classmethod
    def _value_or_default(cls, value: Optional[str], default: str) -> str:
        resolved = value or default
        if not resolved.strip():
            raise ValueError("Knowledge source values must not be empty")
        return resolved

    @classmethod
    def get_name(cls) -> str:
        """Return the configured knowledge source name."""
        return cls._value_or_default(cls._KS_NAME, cls._KS_DEFAULT_NAME)

    @classmethod
    def get_description(cls) -> str:
        """Return the configured knowledge source description."""
        return cls._value_or_default(cls._KS_DESCRIPTION, cls._KS_DEFAULT_DESCRIPTION)

    @classmethod
    def validate(cls) -> None:
        """Ensure both name and description are resolvable."""
        cls.get_name()
        cls.get_description()


class KnowledgeBaseSettings:
    """Centralized settings for the default knowledge base."""

    _KB_DEFAULT_NAME = "kb-name-deafult"
    _KB_DEFAULT_DESCRIPTION = "Agentic RAG sobre mi PDF"
    _KB_DEFAULT_ANSWER_INSTRUCTIONS = (
        "Responde en español, cita siempre la página del PDF."
    )
    _KB_DEFAULT_RETRIEVAL_INSTRUCTIONS = (
        "Responde en español, cita siempre la página del PDF."
    )
    _KB_NAME: Optional[str] = os.getenv("KNOWLEDGE_BASE_NAME")
    _KB_DESCRIPTION: Optional[str] = os.getenv("KNOWLEDGE_BASE_DESCRIPTION")
    _KB_ANSWER_INSTRUCTIONS: Optional[str] = os.getenv(
        "KNOWLEDGE_BASE_ANSWER_INSTRUCTIONS"
    )
    _KB_RETRIEVAL_INSTRUCTIONS: Optional[str] = os.getenv(
        "KNOWLEDGE_BASE_RETRIEVAL_INSTRUCTIONS"
    )

    @classmethod
    def _value_or_default(cls, value: Optional[str], default: str) -> str:
        resolved = value or default
        if not resolved.strip():
            raise ValueError("Knowledge base values must not be empty")
        return resolved

    @classmethod
    def get_name(cls) -> str:
        return cls._value_or_default(cls._KB_NAME, cls._KB_DEFAULT_NAME)

    @classmethod
    def get_description(cls) -> str:
        return cls._value_or_default(cls._KB_DESCRIPTION, cls._KB_DEFAULT_DESCRIPTION)

    @classmethod
    def get_answer_instructions(cls) -> str:
        return cls._value_or_default(
            cls._KB_ANSWER_INSTRUCTIONS, cls._KB_DEFAULT_ANSWER_INSTRUCTIONS
        )

    @classmethod
    def get_retrieval_instructions(cls) -> str:
        return cls._value_or_default(
            cls._KB_RETRIEVAL_INSTRUCTIONS, cls._KB_DEFAULT_RETRIEVAL_INSTRUCTIONS
        )

    @classmethod
    def validate(cls) -> None:
        cls.get_name()
        cls.get_description()
        cls.get_answer_instructions()
        cls.get_retrieval_instructions()

class MCPConnectionSettings:
    """Configuration for exposing the knowledge base as an MCP tool."""

    _PROJECT_RESOURCE_ID: Optional[str] = os.getenv("AI_PROJECT_RESOURCE_ID")
    _PROJECT_CONNECTION_NAME: Optional[str] = os.getenv(
        "AI_PROJECT_CONNECTION_NAME", "rag-mcp-connection"
    )

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
