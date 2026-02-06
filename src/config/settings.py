import os

# Cargar variables de entorno (solo una vez en toda la app)
from dotenv import load_dotenv
load_dotenv()

class AzureSettings:
    """Configuración para Azure OpenAI"""
    
    # Azure OpenAI Settings
    OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    # Azure AI Foundry Settings (para uso futuro)
    AI_PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    AI_MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    @classmethod
    def validate_openai_settings(cls):
        """Valida que las configuraciones de Azure OpenAI estén presentes"""
        if not cls.OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT no está configurado")
        if not cls.OPENAI_CHAT_DEPLOYMENT_NAME:
            raise ValueError("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME no está configurado")
    
    @classmethod
    def validate_ai_foundry_settings(cls):
        """Valida que las configuraciones de Azure AI Foundry estén presentes"""
        if not cls.AI_PROJECT_ENDPOINT:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT no está configurado")
        if not cls.AI_MODEL_DEPLOYMENT_NAME:
            raise ValueError("AZURE_AI_MODEL_DEPLOYMENT_NAME no está configurado")