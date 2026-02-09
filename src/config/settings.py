import os

from dotenv import load_dotenv
load_dotenv()

class AzureSettings:
    """Configuration for Agent"""
    
    # Azure OpenAI Settings
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    # Azure AI Foundry Settings
    AZURE_AI_PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    AZURE_AI_MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")

    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    
    @classmethod
    def azure_openai_settings(cls):
        """Validate that Azure OpenAI configurations are present"""
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not configured")
        if not cls.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME:
            raise ValueError("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME is not configured")
    
    @classmethod
    def azure_ai_foundry_settings(cls):
        """Validate that Azure AI Foundry configurations are present"""
        if not cls.AZURE_AI_PROJECT_ENDPOINT:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT is not configured")
        if not cls.AZURE_AI_MODEL_DEPLOYMENT_NAME:
            raise ValueError("AZURE_AI_MODEL_DEPLOYMENT_NAME is not configured")
    
    @classmethod
    def openai_settings(cls):
        """Validate that OpenAI configurations are present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")
        if not cls.OPENAI_MODEL:
            raise ValueError("OPENAI_MODEL is not configured")
            