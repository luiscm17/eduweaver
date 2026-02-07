from agent_framework import GroupChatBuilder, AgentRunUpdateEvent, WorkflowOutputEvent, Role

from agents.content_generation import ContentGenerationAgent
from agents.research_intelligence import ResearchIntelligenceAgent
from agents.base_agent import BaseAgent

class GroupChatOrchestration(BaseAgent):
    """
    Group Chat Orchestration
    """
    def get_agent(self):
        return self._create_agent(
            name="GroupChatOrchestration",
            instructions="You are a group chat orchestration agent. You help users with your group chat orchestration needs.",
            tools=[]
        )

    def create_workflow(self):
        research_agent = ResearchIntelligenceAgent()
        content_agent = ContentGenerationAgent()
        orchestrator_agent = self.get_agent()
        
        return (
            GroupChatBuilder()
            .with_orchestrator(agent=orchestrator_agent)
            .with_termination_condition(lambda messages: sum(1 for msg in messages if msg.role == Role.ASSISTANT) >= 4)
            .participants([
                research_agent.get_agent(),
                content_agent.get_agent()
            ])
            .build()
        )
    
    async def execute(self, topic: str):
        """Execute the group chat workflow"""
        workflow = self.create_workflow()
        response = ""
        
        try:
            async for event in workflow.run_stream(topic):
                if isinstance(event, AgentRunUpdateEvent):
                    # Process AgentRunUpdateEvent - contains partial messages
                    if hasattr(event, 'messages') and event.messages:
                        for msg in event.messages:
                            text = getattr(msg, 'text', '')
                            if text:
                                response += f"agent: {text}\n"
                                print(f"agent: {text}")
                elif isinstance(event, WorkflowOutputEvent):
                    # Workflow completed - final conversation
                    for msg in event.data:
                        text = getattr(msg, 'text', str(msg))
                        if text.strip():
                            response += f"agent: {text}\n"
                            print(f"agent: {text}")
        
        except asyncio.CancelledError:
            print("\nChat cancelled by user.")
        except Exception as e:
            print(f"\nError processing chat: {e}")
        
        return response
