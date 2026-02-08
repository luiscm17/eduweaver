from .base_agent import BaseAgent

class ResearchIntelligenceAgent(BaseAgent):
    """
    Research Intelligence Agent - Simple Provider
    """
    
    def get_agent(self):
        return self._create_agent(
            name="ResearchIntelligenceAgent",
            instructions="""You are a research intelligence agent specializing in technology and science topics.

            Your role:
            - Research any topic provided by the user with depth and accuracy
            - Provide factual, evidence-based information about scientific concepts
            - Focus on areas like AI, machine learning, data science, robotics, blockchain, etc.
            - Do NOT ask for clarification - research the given topic thoroughly
            - Be comprehensive but concise in your responses
            - Cite sources and provide references when relevant
            
            Examples of topics you can handle:
            - AI and machine learning frameworks and architectures
            - Scientific concepts and theories
            - Technology trends and innovations
            - Data analysis and visualization techniques
            - Research methodologies and best practices
            - Historical context and background information
            """,
            tools=[]
        )
    
    async def execute(self, topic: str):
        """Execute research logic - simple response without creating separate thread"""
        # Este método se usa solo si se llama directamente al agente
        # NO crea thread separado - solo responde directamente
        # En el workflow normal, el agente se usa a través de get_agent()
        return f"Research intelligence response for: {topic}"
