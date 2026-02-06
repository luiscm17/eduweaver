from .base_agent import BaseAgent

class ResearchIntelligence(BaseAgent):
    """
    Research Intelligence Agent
    """
    def get_agent(self):
        return self._create_agent(
            name="ResearchIntelligence",
            instructions="You are a research intelligence agent. You help users with their research needs.",
            tools=[]
        )
    
    async def execute(self, topic: str):
        response = ""
        async for update in self.get_agent().run_stream(topic):
            if update.text:
                response += update.text
        return response
