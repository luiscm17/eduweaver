from abc import ABC, abstractmethod
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient
from config.settings import AzureSettings

class BaseAgent(ABC):
    """
    Base Class for all agents.
    """

    def __init__(self):
        """
        Initialize the base agent.
        """
        self.endpoint = AzureSettings.OPENAI_ENDPOINT
        self.deployment_name = AzureSettings.OPENAI_CHAT_DEPLOYMENT_NAME
        self.credential = AzureCliCredential()
    
    def _create_agent(self, name: str, instructions: str, tools: list):
        """
        Create an agent with the provided name and instructions.
        """
        return AzureOpenAIChatClient(
            endpoint=self.endpoint,
            deployment_name=self.deployment_name,
            credential=self.credential
        ).as_agent(
            name=name,
            instructions=instructions,
            tools=tools
        )

    @abstractmethod
    def get_agent(self):
        """
        Abstract method: each agent must implement this to return its specific agent instance.
        """
        pass

    @abstractmethod
    async def execute(self, *args, **kwargs):
        """
        Abstract method: execute logic for the agent.
        """
        pass
