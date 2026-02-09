import asyncio
from agent_framework import GroupChatBuilder, Role, ChatMessage, WorkflowOutputEvent, Content

from agents.content_generation import ContentGenerationAgent
from agents.research_intelligence import ResearchIntelligenceAgent
from agents.orchestrator_agent import OrchestratorAgent

class GroupChatOrchestration:
    """
    Group Chat Orchestration - Workflow Manager
    """
    
    def __init__(self):
        """Initialize workflow manager with participant agents"""
        self.research_agent = ResearchIntelligenceAgent()
        self.content_agent = ContentGenerationAgent()
        self.orchestrator_agent = OrchestratorAgent()
        self._agents_initialized = False
    
    async def _build_workflow(self):
        """Build the group chat workflow"""
        # Get agents (handle async for research agent)
        orchestrator_agent = self.orchestrator_agent.get_agent()
        research_agent = await self.research_agent.get_agent()
        content_agent = self.content_agent.get_agent()
        
        return (
            GroupChatBuilder()
            .with_orchestrator(agent=orchestrator_agent)
            .with_termination_condition(lambda messages: sum(1 for msg in messages if msg.role == Role.ASSISTANT) >= 6)
            .participants([
                research_agent,
                content_agent
            ])
            .build()
        )
    
    async def execute(self, topic: str):
        """Execute group chat workflow"""
        # Build workflow
        workflow = await self._build_workflow()
        
        # Convert workflow to agent for thread management
        workflow_agent = workflow.as_agent(name="MultiAgentChat")
        
        # Create thread
        thread = workflow_agent.get_new_thread()
        
        # Execute workflow agent with thread
        messages = [ChatMessage(role=Role.USER, contents=[Content.from_text(topic)])]
        
        try:
            full_response = ""
            async for update in workflow_agent.run_stream(messages, thread=thread):
                if update.text:
                    print(update.text, end="", flush=True)
                    full_response += update.text
            if full_response:
                print("\n" + "="*50)
                print("ARTICLE COMPLETE:")
                print(full_response)
                print("="*50)
                return full_response
        except asyncio.CancelledError:
            print("\nChat cancelled by user.")
        except Exception as e:
            print(f"\nError processing chat: {e}")
