from .base_agent import BaseAgent

class ContentGenerationAgent(BaseAgent):
    """
    Content Generation Agent
    """
    def get_agent(self):
        return self._create_agent(
            name="ContentGenerationAgent",
            instructions="You are a content generation agent. You help users with their content generation needs.",
            tools=[]
        )
    
    async def execute(self, topic: str):
        response = ""
        async for update in self.get_agent().run_stream(topic):
            if update.text:
                response += update.text
        return response
