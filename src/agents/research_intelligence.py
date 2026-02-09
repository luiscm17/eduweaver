from agent_framework import HostedWebSearchTool
from agent_framework.azure import AzureAIProjectAgentProvider
from azure.identity.aio import AzureCliCredential
from tools.web_search_properties import get_academic_search_properties

class ResearchIntelligenceAgent:
    """
    Research Intelligence Agent - Azure AI Project Provider with Web Search
    """
    
    def __init__(self):
        """Initialize agent with Azure AI Project Provider and web search capabilities"""
        self.credential = AzureCliCredential()
        self.provider = AzureAIProjectAgentProvider(credential=self.credential)
        self.agent = None
    
    async def get_agent(self):
        """Get or create the agent with web search capabilities"""
        if self.agent is None:
            # Usar propiedades académicas modularizadas
            search_properties = get_academic_search_properties()
            
            self.agent = await self.provider.create_agent(
                name="ResearchIntelligenceAgent",
                instructions="""You are a research intelligence agent specializing in technology and science topics.

                Your role:
                - Research any topic provided by the user with depth and accuracy
                - Provide factual, evidence-based information about scientific concepts
                - Focus on areas like AI, machine learning, data science, robotics, blockchain, etc.
                - Use web search to find current, accurate information
                - Be comprehensive but concise in your responses
                - Cite sources and provide references when relevant
                
                Examples of topics you can handle:
                - AI and machine learning frameworks and architectures
                - Scientific concepts and theories
                - Technology trends and innovations
                - Data analysis and visualization techniques
                - Research methodologies and best practices
                - Historical context and background information
                
                WEB SEARCH GUIDELINES:
                - Use the web search tool to find current and accurate information
                - Always verify information from multiple sources when possible
                - Provide up-to-date information on technology topics
                - Include recent developments and trends in your research
                """,
                tools=[HostedWebSearchTool(additional_properties=search_properties)]
            )
        return self.agent
    
    async def execute(self, topic: str):
        """Execute research logic - simple response without creating separate thread"""
        return topic
